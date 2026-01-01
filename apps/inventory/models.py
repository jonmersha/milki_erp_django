from django.db import models, transaction
from django.forms import ValidationError
from django.utils import timezone
from apps.core.base import BaseModel
from apps.core.models import Company, Factory
from apps.core.utility.uuidgen import generate_custom_id

# -----------------------------
# Warehouse
# -----------------------------
class Warehouse(BaseModel):
    STATUS_CHOICES = [('active', 'Active'), ('inactive', 'Inactive')]
    id = models.BigAutoField(primary_key=True)
    tracker = models.CharField(max_length=16, editable=False, unique=True, db_index=True)
    factory = models.ForeignKey(Factory, on_delete=models.PROTECT, related_name='warehouses')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    capacity = models.PositiveIntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def save(self, *args, **kwargs):
        if not self.tracker:
            self.tracker = generate_custom_id(prefix="WRH", partition=timezone.now().strftime("%Y%m%d"), length=16)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.tracker})"

# -----------------------------
# Product
# -----------------------------
class Product(BaseModel):
    UNIT_CHOICES = [
        ('kg', 'Kilogram'), ('g', 'Gram'), ('l', 'Liter'),
        ('ml', 'Milliliter'), ('pcs', 'Pieces'), ('box', 'Box'),
    ]

    id = models.BigAutoField(primary_key=True)
    tracker = models.CharField(max_length=16, editable=False, unique=True, db_index=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    unit_of_measure = models.CharField(max_length=20, choices=UNIT_CHOICES)
    status = models.CharField(max_length=10, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='products')

    def save(self, *args, **kwargs):
        if not self.tracker:
            self.tracker = generate_custom_id(prefix="PRD", partition=timezone.now().strftime("%Y%m%d"), length=16)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.tracker})"

# -----------------------------
# Stock (The Bridge)
# -----------------------------
class Stock(BaseModel):
    id = models.BigAutoField(primary_key=True)
    tracker = models.CharField(max_length=16, editable=False, unique=True, db_index=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='stocks')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='stocks')
    quantity = models.IntegerField(default=0)
    locked_amount = models.IntegerField(default=0)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    total_value = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['warehouse', 'product'], name='unique_stock_item')
        ]

    def save(self, *args, **kwargs):
        if not self.tracker:
            self.tracker = generate_custom_id(prefix="STK", length=16)
        if self.unit_price and self.quantity:
            self.total_value = self.unit_price * self.quantity
        super().save(*args, **kwargs)

# -----------------------------
# Inventory Movement Log
# -----------------------------
class InventoryMovementLog(BaseModel):
    id = models.BigAutoField(primary_key=True)
    tracker = models.CharField(max_length=16, editable=False, unique=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    movement_type = models.CharField(max_length=20, choices=[('inbound', 'Inbound'), ('outbound', 'Outbound')])
    reason = models.CharField(max_length=20, choices=[('purchase', 'Purchase'), ('sales', 'Sales'), ('transfer', 'Transfer')])
    source_warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='outgoing_logs', null=True)
    destination_warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='incoming_logs', null=True)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.tracker:
            self.tracker = generate_custom_id(prefix="MOV", length=16)
        super().save(*args, **kwargs)

# -----------------------------
# Stock Transfer
# -----------------------------
class StockTransfer(BaseModel):
    id = models.BigAutoField(primary_key=True)
    tracker = models.CharField(max_length=16, editable=False, unique=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    source_warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name="transfers_out")
    destination_warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name="transfers_in")
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=[('PENDING', 'Pending'), ('COMPLETED', 'Completed'), ('CANCELLED', 'Cancelled')], default='PENDING')

    def save(self, *args, **kwargs):
        if not self.tracker:
            self.tracker = generate_custom_id(prefix="TRF", length=16)
        
        with transaction.atomic():
            if self._state.adding:
                # Lock stock at source upon creation
                source_stock = Stock.objects.select_for_update().get(warehouse=self.source_warehouse, product=self.product)
                if source_stock.quantity < self.quantity:
                    raise ValidationError("Insufficient stock.")
                source_stock.quantity -= self.quantity
                source_stock.locked_amount += self.quantity
                source_stock.save()

            elif self.status == 'COMPLETED':
                # Move from locked to destination
                source_stock = Stock.objects.select_for_update().get(warehouse=self.source_warehouse, product=self.product)
                dest_stock, _ = Stock.objects.get_or_create(warehouse=self.destination_warehouse, product=self.product)
                
                source_stock.locked_amount -= self.quantity
                dest_stock.quantity += self.quantity
                
                source_stock.save()
                dest_stock.save()
                
                # Log Movements
                InventoryMovementLog.objects.create(product=self.product, quantity=self.quantity, movement_type='outbound', reason='transfer', source_warehouse=self.source_warehouse)
                InventoryMovementLog.objects.create(product=self.product, quantity=self.quantity, movement_type='inbound', reason='transfer', destination_warehouse=self.destination_warehouse)

        super().save(*args, **kwargs)