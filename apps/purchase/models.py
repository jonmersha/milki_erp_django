from django.db import models, transaction
from django.utils import timezone
from decimal import Decimal
from apps.core.base import BaseModel
from apps.core.utility.uuidgen import generate_custom_id
from apps.inventory.models import InventoryMovementLog, Product, Stock, Warehouse
from .managers import PurchaseOrderManager

class Supplier(BaseModel):
    STATUS_CHOICES = [('active', 'Active'), ('inactive', 'Inactive')]
    id = models.CharField(max_length=16, primary_key=True, editable=False, unique=True)
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


class PurchaseOrder(BaseModel):
    STATUS_CHOICES = [('pending', 'Pending'), ('inactive', 'Inactive'), ('received', 'Received')]
    id = models.CharField(max_length=16, primary_key=True, editable=False, unique=True)
    destination_store = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='purchase_orders')
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    objects = PurchaseOrderManager()
    
    def save(self, *args, **kwargs):
        if not self.id:
            partition = timezone.now().strftime("%Y%m%d")
            self.id = generate_custom_id(prefix="PO", partition=partition, length=16)
        super().save(*args, **kwargs)

class PurchaseOrderItem(BaseModel):
    STATUS_CHOICES = [('pending', 'Pending'), ('received', 'Received')]
    id = models.CharField(max_length=16, primary_key=True, editable=False, unique=True)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if not self.id:
                partition = timezone.now().strftime("%Y%m%d")
                self.id = generate_custom_id(prefix="POI", partition=partition, length=16)

            self.quantity = int(self.quantity)
            self.unit_price = Decimal(self.unit_price)

            # --- Merge logic for Pending items ---
            duplicate = PurchaseOrderItem.objects.select_for_update().filter(
                purchase_order=self.purchase_order,
                product=self.product,
                status='pending'
            ).exclude(pk=self.pk).first()

            if duplicate:
                duplicate.quantity += self.quantity
                duplicate.unit_price = self.unit_price
                duplicate.save(update_fields=['quantity', 'unit_price'])
                return # Stop save, we updated the existing one

            super().save(*args, **kwargs)

            if self.status == "received":
                self._update_stock_and_log(self)

    def _update_stock_and_log(self, item):
        warehouse = item.purchase_order.destination_store
        stock, _ = Stock.objects.select_for_update().get_or_create(
            warehouse=warehouse,
            product=item.product,
            defaults={"quantity": 0, "locked_amount": 0, "unit_price": item.unit_price, "total_value": 0}
        )
        stock.quantity += item.quantity
        stock.unit_price = item.unit_price
        stock.total_value = stock.quantity * stock.unit_price
        stock.save()

        InventoryMovementLog.objects.create(
            product=item.product, quantity=item.quantity, movement_type='inbound',
            reason='purchase', destination_warehouse=warehouse, unit_price=item.unit_price
        )
class GoodsReceivingNote(BaseModel):
    id = models.CharField(max_length=16, primary_key=True, editable=False, unique=True)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.PROTECT, related_name='grns')
    received_by = models.CharField(max_length=100) # Name of clerk
    delivery_note_number = models.CharField(max_length=50, blank=True)
    received_date = models.DateTimeField(default=timezone.now)
    remarks = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            partition = timezone.now().strftime("%Y%m%d")
            self.id = generate_custom_id(prefix="GRN", partition=partition, length=16)
        super().save(*args, **kwargs)

class GRNItem(BaseModel):
    grn = models.ForeignKey(GoodsReceivingNote, on_delete=models.CASCADE, related_name='items')
    po_item = models.ForeignKey(PurchaseOrderItem, on_delete=models.PROTECT)
    quantity_received = models.IntegerField()

    def save(self, *args, **kwargs):
        with transaction.atomic():
            # Trigger the status change on the PO Item to update stock
            # Your existing POItem.save() handles stock and movement logs
            item = self.po_item
            item.status = 'received'
            item.quantity = self.quantity_received # Optional: update to actual quantity received
            item.save()
            super().save(*args, **kwargs)