from django.db import models
from django.forms import ValidationError
from django.utils import timezone
from core.base import BaseModel
from core.models import Company, Factory
from core.utility.uuidgen import generate_custom_id
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
            self.id = generate_custom_id(prefix="WRH", partition=partition, length=16)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} | {self.name} ({self.factory.name})"


# -----------------------------
# Product Package
# -----------------------------
class ProductPackage(BaseModel):
    id = models.CharField(
        primary_key=True,
        max_length=16,
        editable=False,
        unique=True
    )
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    size = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Physical size or capacity, e.g., 500g, 1L, 20kg, etc."
    )
    dimensions = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Optional package dimensions (LxWxH in cm)."
    )
    weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Weight in kilograms, if applicable."
    )

    class Meta:
        verbose_name = "Product Package"
        verbose_name_plural = "Product Packages"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.id:
            partition = timezone.now().strftime("%Y%m%d")
            self.id = generate_custom_id(prefix="PKG", partition=partition, length=16)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.size or 'N/A'})"


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
        ('na', 'Not Applicable'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    id = models.CharField(
        primary_key=True,
        max_length=16,
        editable=False,
        unique=True
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    unit_of_measure = models.CharField(max_length=20, choices=UNIT_CHOICES)
    package = models.ForeignKey(
        ProductPackage, on_delete=models.PROTECT, blank=True, null=True,
        help_text="Optional reference to a defined package type"
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='products')

    def save(self, *args, **kwargs):
        if not self.id:
            partition = timezone.now().strftime("%Y%m%d")
            self.id = generate_custom_id(prefix="PRD", partition=partition, length=16)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.id})"


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
                InventoryMovementLog.objects.create(
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





# class StockTransfer(BaseModel):
#     TRANSFER_STATUS = [
#         ('PENDING', 'Pending'),
#         ('IN_PROGRESS', 'In Progress'),
#         ('COMPLETED', 'Completed'),
#         ('CANCELLED', 'Cancelled'),
#     ]

#     id = models.CharField(
#         max_length=20,
#         primary_key=True,
#         editable=False,
#         unique=True
#     )

#     product = models.ForeignKey(
#         'Product',
#         on_delete=models.CASCADE,
#         related_name='stock_transfers'
#     )

#     quantity = models.DecimalField(max_digits=12, decimal_places=2)
#     unit_of_measure = models.CharField(max_length=20, default='pcs')

#     source_warehouse = models.ForeignKey(
#         'Warehouse',
#         on_delete=models.CASCADE,
#         related_name='outgoing_transfers'
#     )

#     destination_warehouse = models.ForeignKey(
#         'Warehouse',
#         on_delete=models.CASCADE,
#         related_name='incoming_transfers'
#     )

#     status = models.CharField(
#         max_length=20,
#         choices=TRANSFER_STATUS,
#         default='PENDING'
#     )

#     requested_date = models.DateTimeField(auto_now_add=True)
#     authorized_date = models.DateTimeField(null=True, blank=True)
#     completed_date = models.DateTimeField(null=True, blank=True)
#     remarks = models.TextField(blank=True, null=True)

#     class Meta:
#         db_table = 'stock_transfer'
#         ordering = ['-requested_date']
#         verbose_name = 'Stock Transfer'
#         verbose_name_plural = 'Stock Transfers'

#     def __str__(self):
#         return f"{self.id} - {self.product.name} ({self.quantity} {self.unit_of_measure})"

#     def mark_completed(self):
#         """Mark the transfer as completed and record completion time."""
#         if self.status != 'COMPLETED':
#             self.status = 'COMPLETED'
#             self.completed_date = timezone.now()
#             self.save(update_fields=['status', 'completed_date'])

#     def save(self, *args, **kwargs):
#         if not self.id:
#             partition = timezone.now().strftime("%Y%m%d")
#             self.id = generate_custom_id(prefix="TRN", partition=partition, length=16)
#         super().save(*args, **kwargs)

#     def clean(self):
#         """Ensure source and destination warehouses are different."""
#         if self.source_warehouse == self.destination_warehouse:
#             raise ValidationError("Source and destination warehouse must be different.")
from django.db import models
from django.utils import timezone
from core.base import BaseModel
from core.utility.uuidgen import generate_custom_id
from inventory.models import Stock  # assuming Stock model exists in inventory app
from django.core.exceptions import ValidationError

class StockTransfer(BaseModel):
    TRANSFER_STATUS = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    id = models.CharField(max_length=20, primary_key=True, editable=False, unique=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='stock_transfers')
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    unit_of_measure = models.CharField(max_length=20, default='pcs')
    source_warehouse = models.ForeignKey('Warehouse', on_delete=models.CASCADE, related_name='outgoing_transfers')
    destination_warehouse = models.ForeignKey('Warehouse', on_delete=models.CASCADE, related_name='incoming_transfers')
    status = models.CharField(max_length=20, choices=TRANSFER_STATUS, default='PENDING')
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

    def clean(self):
        """Ensure source and destination warehouses are different."""
        if self.source_warehouse == self.destination_warehouse:
            raise ValidationError("Source and destination warehouse must be different.")

    def save(self, *args, **kwargs):
        if not self.id:
            partition = timezone.now().strftime("%Y%m%d")
            self.id = generate_custom_id(prefix="TRN", partition=partition, length=16)
        super().save(*args, **kwargs)

    def mark_completed(self):
        """
        Mark the transfer as completed, record completion time,
        and update the stock quantities for source and destination warehouses.
        """
        if self.status == 'COMPLETED':
            return  # Already completed

        # Fetch or create stock records
        source_stock, _ = Stock.objects.get_or_create(
            product=self.product,
            warehouse=self.source_warehouse,
            defaults={'quantity': 0}
        )
        destination_stock, _ = Stock.objects.get_or_create(
            product=self.product,
            warehouse=self.destination_warehouse,
            defaults={'quantity': 0}
        )

        # Check if source has enough stock
        if source_stock.quantity < self.quantity:
            raise ValidationError(f"Not enough stock in source warehouse '{self.source_warehouse.name}'.")

        # Adjust stock quantities
        source_stock.quantity -= self.quantity
        source_stock.save(update_fields=['quantity', 'last_updated'])

        destination_stock.quantity += self.quantity
        destination_stock.save(update_fields=['quantity', 'last_updated'])

        # Mark transfer as completed
        self.status = 'COMPLETED'
        self.completed_date = timezone.now()
        self.save(update_fields=['status', 'completed_date'])
