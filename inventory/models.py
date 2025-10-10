from django.db import models
from django.utils import timezone
from core.base import BaseModel
from core.models import Company, Factory
from core.utility.uuidgen import generate_custom_id
# from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings


# -----------------------------
# Warehouse
# -----------------------------


class Warehouse(BaseModel):
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

    # Factory is the only parent
    factory = models.ForeignKey(
        Factory,
        on_delete=models.PROTECT,
        related_name='warehouses',
        help_text="The parent factory this warehouse belongs to."
    )

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    capacity = models.PositiveIntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def save(self, *args, **kwargs):
        if not self.id:
            partition = timezone.now().strftime("%Y%m%d")
            self.id = generate_custom_id(prefix="WH", partition=partition, length=16)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} | {self.name} ({self.factory.name})"


# -----------------------------
# Product Package
# -----------------------------
class ProductPackage(BaseModel):
    id = models.CharField(
        max_length=16,
        primary_key=True,
        editable=False,
        unique=True
    )
    name = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.id:
            partition = timezone.now().strftime("%Y%m%d")
            self.id = generate_custom_id(prefix="PKG", partition=partition, length=16)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# -----------------------------
# Product
# -----------------------------
class Product(BaseModel):
    UNIT_CHOICES = [
        ('kg', 'Kilogram'),
        ('g', 'Gram'),
        ('l', 'Liter'),
        ('ml', 'Milliliter'),
        ('pcs', 'Pieces'),
        ('box', 'Box'),
        ('pack', 'Pack'),
        ('NA', 'NA'),
    ]

    PACKAGE_SIZE_CHOICES = [
        ('NA', 'NA'),
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
    ]

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
    description = models.TextField(blank=True, null=True)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    unit_of_measure = models.CharField(max_length=50, choices=UNIT_CHOICES)
    package_size = models.CharField(max_length=50, choices=PACKAGE_SIZE_CHOICES, blank=True, null=True)
    package_name = models.ForeignKey(ProductPackage, on_delete=models.PROTECT, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True, null=True)
    factory = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='products')

    def save(self, *args, **kwargs):
        if not self.id:
            partition = timezone.now().strftime("%Y%m%d")
            self.id = generate_custom_id(prefix="PRD", partition=partition, length=16)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} | {self.name}"


# -----------------------------
# Stock
# -----------------------------
class Stock(BaseModel):
    id = models.CharField(
        max_length=16,
        primary_key=True,
        editable=False,
        unique=True
    )
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    remarks = models.TextField(blank=True, null=True)
    locked_amount = models.IntegerField(default=0)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    total_value = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    minimum_threshold = models.IntegerField(default=0)

    class Meta:
        unique_together = ('product', 'warehouse')

    def save(self, *args, **kwargs):
        if not self.id:
            partition = timezone.now().strftime("%Y%m%d")
            self.id = generate_custom_id(prefix="INV", partition=partition, length=16)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} | {self.product.name} in {self.warehouse.name} - {self.quantity}"
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['warehouse', 'product'], name='Only_one_type_per_warehouse')
        ]

# -----------------------------
# Inventory Movement
# -----------------------------


class InventoryMovementLog(BaseModel):
    MOVEMENT_TYPE_CHOICES = [
    ('inbound', 'Inbound'),
    ('outbound', 'Outbound'),
    ]

    MOVEMENT_REASON_CHOICES = [
    ('purchase', 'Purchase'),
    ('sales', 'Sales'),
    ('transfer', 'Transfer'),
    ('processing', 'Processing'),
    ]

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
    product = models.ForeignKey('Product', on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()
    movement_type = models.CharField(
        max_length=20,
        choices=MOVEMENT_TYPE_CHOICES
    )
    reason = models.CharField(
        max_length=20,
        choices=MOVEMENT_REASON_CHOICES,
        help_text="Reason for this inventory movement"
    )
    warehouse = models.ForeignKey(
        'Warehouse',
        on_delete=models.PROTECT,
        related_name='movement_source_warehouse',
        null=True,
        blank=True
    )
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )

    def save(self, *args, **kwargs):
        # Generate custom ID if not exists
        if not self.id:
            partition = timezone.now().strftime("%Y%m%d")
            self.id = generate_custom_id(prefix="MOV", partition=partition, length=16)

        super().save(*args, **kwargs)

        # Handle transfers automatically
        if self.reason == 'transfer':
            # Only create the counterpart if it does not exist
            if self.movement_type == 'outbound' and self.destination_warehouse:
                # Create corresponding inbound movement
                InventoryMovement.objects.create(
                    product=self.product,
                    quantity=self.quantity,
                    movement_type='inbound',
                    reason='transfer',
                    source_warehouse=self.source_warehouse,
                    destination_warehouse=self.destination_warehouse,
                    unit_price=self.unit_price,
                    remarks=f"Transfer inbound for {self.id}",
                    status=self.status
                )

    def __str__(self):
        warehouse = self.source_warehouse or self.destination_warehouse
        return f"{self.id} | {self.movement_type} ({self.reason}) - {self.product.name} ({self.quantity}) | {warehouse}"



# Ensure you have this helper defined somewhere in utils/helpers.py, for example
# def generate_custom_id(prefix: str, partition: str, length: int) -> str:
#     import uuid
#     unique_part = uuid.uuid4().hex[:length - len(prefix) - len(partition) - 1].upper()
#     return f"{prefix}{partition}{unique_part}"


class StockTransfer(BaseModel):
    TRANSFER_STATUS = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    id = models.CharField(
        max_length=20,
        primary_key=True,
        editable=False,
        unique=True
    )

    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='stock_transfers'
    )

    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    unit_of_measure = models.CharField(max_length=20, default='pcs')

    source_warehouse = models.ForeignKey(
        'Warehouse',
        on_delete=models.CASCADE,
        related_name='outgoing_transfers'
    )

    destination_warehouse = models.ForeignKey(
        'Warehouse',
        on_delete=models.CASCADE,
        related_name='incoming_transfers'
    )

    status = models.CharField(
        max_length=20,
        choices=TRANSFER_STATUS,
        default='PENDING'
    )

    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='requested_transfers'
    )

    requested_date = models.DateTimeField(auto_now_add=True)
    authorized_date = models.DateTimeField(null=True, blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)

    remarks = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'stock_transfer'
        ordering = ['-requested_date']
        verbose_name = 'Stock Transfer'
        verbose_name_plural = 'Stock Transfers'

    def __str__(self):
        return f"{self.id} - {self.product.name} ({self.quantity} {self.unit_of_measure})"

    def mark_completed(self):
        """Mark the transfer as completed and record completion time."""
        if self.status != 'COMPLETED':
            self.status = 'COMPLETED'
            self.completed_date = timezone.now()
            self.save(update_fields=['status', 'completed_date'])

    def save(self, *args, **kwargs):
        """Generate a unique transfer ID if not set."""
        if not self.id:
            partition = timezone.now().strftime("%Y%m%d")
            from utils.helpers import generate_custom_id
            self.id = generate_custom_id(prefix="TRN", partition=partition, length=16)
        super().save(*args, **kwargs)
