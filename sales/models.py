from django.db import models

from poso.models import Customer

class SalerOrder(models.Model):
    id=models.CharField(max_length=20,primary_key=True,editable=False)
    customer=models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        null=False,blank=False,editable=False)
    order_status=models.CharField(default='Pending')
    order_date=models.DateTimeField(auto_now=True)



from django.db import models, transaction
from django.utils import timezone
from django.core.exceptions import ValidationError
from core.models import BaseModel, Warehouse
from core.utility.uuidgen import generate_custom_id
from inventory.models import Stock, InventoryMovementLog
# from finance.models import Payment
from decimal import Decimal


class Customer(BaseModel):
    id = models.CharField(max_length=16, primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default='active')

    def save(self, *args, **kwargs):
        if not self.id:
            partition = timezone.now().strftime("%Y%m%d")
            self.id = generate_custom_id(prefix="CUS", partition=partition, length=16)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SalesOrder(BaseModel):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('CONFIRMED', 'Confirmed'),
        ('PARTIALLY_DELIVERED', 'Partially Delivered'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('UNPAID', 'Unpaid'),
        ('PARTIALLY_PAID', 'Partially Paid'),
        ('PAID', 'Paid'),
    ]

    id = models.CharField(max_length=16, primary_key=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='orders')
    order_date = models.DateField(default=timezone.now)
    source_store = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='DRAFT')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='UNPAID')
    total_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    remarks = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            partition = timezone.now().strftime("%Y%m%d")
            self.id = generate_custom_id(prefix="SO", partition=partition, length=16)
        super().save(*args, **kwargs)

    # --- Helpers ---
    def recalc_total(self):
        total = self.items.aggregate(total=models.Sum(models.F('quantity') * models.F('unit_price')))['total'] or Decimal('0.00')
        self.total_amount = total
        self.save(update_fields=['total_amount'])

    def update_status(self):
        items = self.items.all()
        if not items.exists():
            self.status = 'DRAFT'
        elif all(i.status == 'DELIVERED' for i in items):
            self.status = 'DELIVERED'
        elif any(i.status == 'DELIVERED' for i in items):
            self.status = 'PARTIALLY_DELIVERED'
        elif all(i.status == 'CANCELLED' for i in items):
            self.status = 'CANCELLED'
        else:
            self.status = 'CONFIRMED'
        self.save(update_fields=['status'])

    def update_payment_status(self):
        total_paid = sum(p.amount for p in self.payments.filter(status='paid'))
        if total_paid <= 0:
            new_status = 'UNPAID'
        elif total_paid < self.total_amount:
            new_status = 'PARTIALLY_PAID'
        else:
            new_status = 'PAID'
        self.payment_status = new_status
        self.save(update_fields=["payment_status"])
        self.items.update(payment_status=new_status)

    def __str__(self):
        return f"Sales Order {self.id} - {self.customer.name}"


class SalesOrderItem(BaseModel):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('UNPAID', 'Unpaid'),
        ('PARTIALLY_PAID', 'Partially Paid'),
        ('PAID', 'Paid'),
    ]

    id = models.CharField(max_length=16, primary_key=True, editable=False)
    sales_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('inventory.Product', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='UNPAID')
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [models.Index(fields=['sales_order', 'product'])]

    @property
    def total_price(self):
        return self.quantity * self.unit_price

    def save(self, *args, **kwargs):
        if not self.id:
            partition = timezone.now().strftime("%Y%m%d")
            self.id = generate_custom_id(prefix="SOI", partition=partition, length=16)

        with transaction.atomic():
            is_new = self._state.adding
            stock = Stock.objects.select_for_update().filter(
                warehouse=self.sales_order.source_store, product=self.product
            ).first()

            if not stock:
                raise ValidationError("Stock not found for this product.")

            if is_new:
                if stock.quantity < self.quantity:
                    raise ValidationError("Insufficient stock.")
                stock.quantity -= self.quantity
                stock.locked_amount += self.quantity
                stock.save(update_fields=["quantity", "locked_amount"])
            else:
                prev = SalesOrderItem.objects.select_for_update().get(pk=self.pk)
                if prev.status == "DELIVERED":
                    raise ValidationError("Delivered items cannot be modified.")
                if self.status == "DELIVERED" and prev.status != "DELIVERED":
                    self._deliver(stock)
                elif self.status == "CANCELLED" and prev.status != "CANCELLED":
                    self._cancel(stock)

            super().save(*args, **kwargs)
            self.sales_order.recalc_total()
            self.sales_order.update_status()

    def _deliver(self, stock):
        stock.locked_amount -= self.quantity
        stock.save(update_fields=["locked_amount"])
        InventoryMovementLog.objects.create(
            product=self.product,
            quantity=self.quantity,
            movement_type='outbound',
            reason='sales',
            source_warehouse=self.sales_order.source_store,
            remarks=f"Delivered via Sales Order {self.sales_order.id}"
        )

    def _cancel(self, stock):
        stock.quantity += self.quantity
        stock.locked_amount -= self.quantity
        stock.save(update_fields=["quantity", "locked_amount"])

    def __str__(self):
        return f"{self.product} ({self.quantity})"


# Payment is defined in finance.models — you can link it with a ForeignKey
# sales_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name='payments')
# It will automatically update SalesOrder.payment_status on save.
    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new and self.status == 'paid':
            if self.sales_order:
                self.sales_order.update_payment_status()
            elif self.purchase_order:
                self.purchase_order.update_payment_status()
