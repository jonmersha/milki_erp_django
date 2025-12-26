from datetime import timezone
from decimal import Decimal
from django.db import models,transaction

from apps.core.base import BaseModel
from apps.core.utility.uuidgen import generate_custom_id
from apps.inventory.models import InventoryMovementLog, Product, Stock, Warehouse

# Create your models here.
class Supplier(BaseModel):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    id = models.CharField(
        max_length=16,
        primary_key=True,
        editable=False,
        unique=True
    )
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True, null=True)
    def save(self, *args, **kwargs):
        if not self.id:
            partition = timezone.now().strftime("%Y%m%d")
            self.id = generate_custom_id(prefix="SUP", partition=partition, length=16)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name

# ------------------------------------------------
# Purchase order
# ------------------------------------------------
class PurchaseOrder(BaseModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('inactive', 'Inactive'),
        ('received','Received')
    ]
    id = models.CharField(
        max_length=16,
        primary_key=True,
        editable=False,
        unique=True
    )
    destination_store = models.ForeignKey(
        Warehouse,
        on_delete=models.PROTECT,
        related_name='purchase_orders'
    )
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    def save(self, *args, **kwargs):
        if not self.id:
            partition = timezone.now().strftime("%Y%m%d")
            self.id = generate_custom_id(prefix="PO", partition=partition, length=16)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"PO-{self.id}"
    
class PurchaseOrderItem(BaseModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('received', 'Received'),
    ]

    id = models.CharField(
        max_length=16,
        primary_key=True,
        editable=False,
        unique=True
    )
    purchase_order = models.ForeignKey(
        PurchaseOrder,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def save(self, *args, **kwargs):
        with transaction.atomic():
            # --- Generate ID if new ---
            if not self.id:
                partition = timezone.now().strftime("%Y%m%d")
                self.id = generate_custom_id(prefix="POI", partition=partition, length=16)

            # --- Ensure proper types ---
            self.quantity = int(self.quantity)
            self.unit_price = Decimal(self.unit_price)

            # --- Handle duplicates manually ---
            duplicate = PurchaseOrderItem.objects.select_for_update().filter(
                purchase_order=self.purchase_order,
                product=self.product
            ).exclude(pk=self.pk).first()

            if duplicate and duplicate.status == "pending":
                # Merge quantities and update unit price
                duplicate.quantity += self.quantity
                duplicate.unit_price = self.unit_price
                if self.status == "received":
                    duplicate.status = "received"
                    self._update_stock_and_log(duplicate)
                duplicate.save(update_fields=['quantity', 'unit_price', 'status'])
                return  # Exit without creating new row

            # --- Save normally (new or received duplicate) ---
            super().save(*args, **kwargs)

            if self.status == "received":
                self._update_stock_and_log(self)

    def _update_stock_and_log(self, item):
        warehouse = item.purchase_order.destination_store
        stock, _ = Stock.objects.select_for_update().get_or_create(
            warehouse=warehouse,
            product=item.product,
            defaults={
                "quantity": 0,
                "locked_amount": 0,
                "unit_price": Decimal(item.unit_price),
                "total_value": 0,
                "remarks": f"Created via PO {item.purchase_order.id}"
            }
        )

        stock.quantity += item.quantity
        stock.unit_price = Decimal(item.unit_price)
        stock.total_value = stock.quantity * stock.unit_price
        stock.remarks = f"Updated via PO {item.purchase_order.id}"
        stock.save(update_fields=['quantity', 'unit_price', 'total_value', 'remarks'])

        InventoryMovementLog.objects.create(
            product=item.product,
            quantity=item.quantity,
            movement_type='inbound',
            reason='purchase',
            destination_warehouse=warehouse,
            unit_price=item.unit_price,
            remarks=f"Received from PO {item.purchase_order.id}"
        )

    @property
    def total_price(self):
        return Decimal(self.quantity) * Decimal(self.unit_price)

    @property
    def warehouse_info(self):
        warehouse = self.purchase_order.destination_store
        return {
            "id": warehouse.id,
            "name": warehouse.name,
            "code": getattr(warehouse, "code", None),
            "address": getattr(warehouse, "address", None)
        }