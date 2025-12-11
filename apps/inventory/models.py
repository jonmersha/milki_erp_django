from django.db import models,transaction
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
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPE_CHOICES)
    reason = models.CharField(max_length=20, choices=MOVEMENT_REASON_CHOICES)
    source_warehouse = models.ForeignKey(
        'Warehouse',
        on_delete=models.PROTECT,
        related_name='movement_source_warehouse',
        null=True, blank=True
    )
    destination_warehouse = models.ForeignKey(
        'Warehouse',
        on_delete=models.PROTECT,
        related_name='movement_destination_warehouse',
        null=True, blank=True
    )
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def save(self, *args, **kwargs):
        # Generate custom ID if not exists
        if not self.id:
            partition = timezone.now().strftime("%Y%m%d")
            self.id = generate_custom_id(prefix="MOV", partition=partition, length=16)
        super().save(*args, **kwargs)

    def __str__(self):
        direction = "→" if self.movement_type == "outbound" else "←"
        return f"{self.id} | {self.product.name} {direction} {self.quantity} ({self.reason})"
# ------------------------------------------
#Stock Tranfer
#-------------------------------------------

class StockTransfer(BaseModel):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    id = models.CharField(max_length=16, primary_key=True, editable=False, unique=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    source_warehouse = models.ForeignKey(
        Warehouse, on_delete=models.PROTECT, related_name="outgoing_transfers"
    )
    destination_warehouse = models.ForeignKey(
        Warehouse, on_delete=models.PROTECT, related_name="incoming_transfers"
    )
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['id'], name='unique_stock_transfer_id')
        ]

    def __str__(self):
        return f"Transfer {self.id} | {self.product.name} from {self.source_warehouse.name} to {self.destination_warehouse.name}"

    def clean(self):
        if self.source_warehouse == self.destination_warehouse:
            raise ValidationError("Source and destination warehouses must be different.")

    def save(self, *args, **kwargs):
        if not self.id:
            partition = timezone.now().strftime("%Y%m%d")
            self.id = generate_custom_id(prefix="TRF", partition=partition, length=16)

        self.clean()

        with transaction.atomic():
            is_new = self._state.adding
            source_stock = Stock.objects.select_for_update().filter(
                warehouse=self.source_warehouse, product=self.product
            ).first()

            if not source_stock:
                raise ValidationError("Source stock record not found.")

            if is_new:
                # --- On creation: lock and decrement source ---
                if source_stock.quantity < self.quantity:
                    raise ValidationError("Insufficient stock in source warehouse.")
                source_stock.quantity -= self.quantity
                source_stock.locked_amount += self.quantity
                source_stock.save(update_fields=["quantity", "locked_amount"])
            else:
                previous = StockTransfer.objects.select_for_update().get(pk=self.pk)

                # --- Completed transfers cannot be changed ---
                if previous.status == "COMPLETED":
                    raise ValidationError("Completed transfers cannot be modified.")
                # --- Cancelled transfers cannot be changed ---
                if previous.status == "CANCELLED":
                    raise ValidationError("Cancelled transfers cannot be modified.")

                # --- Handle cancel ---
                if self.status == "CANCELLED":
                    source_stock.quantity += self.quantity
                    source_stock.locked_amount -= self.quantity
                    source_stock.save(update_fields=["quantity", "locked_amount"])

                # --- Handle completion ---
                elif self.status == "COMPLETED":
                    dest_stock, _ = Stock.objects.get_or_create(
                        warehouse=self.destination_warehouse,
                        product=self.product,
                        defaults={"quantity": 0, "locked_amount": 0},
                    )
                    dest_stock.quantity += self.quantity
                    dest_stock.save(update_fields=["quantity"])

                    source_stock.locked_amount -= self.quantity
                    source_stock.save(update_fields=["locked_amount"])

                    # ✅ Log both outbound and inbound movements
                    InventoryMovementLog.objects.create(
                        product=self.product,
                        quantity=self.quantity,
                        movement_type='outbound',
                        reason='transfer',
                        source_warehouse=self.source_warehouse,
                        destination_warehouse=self.destination_warehouse,
                        remarks=f"Outbound transfer from {self.source_warehouse.name} to {self.destination_warehouse.name}"
                    )
                    InventoryMovementLog.objects.create(
                        product=self.product,
                        quantity=self.quantity,
                        movement_type='inbound',
                        reason='transfer',
                        source_warehouse=self.source_warehouse,
                        destination_warehouse=self.destination_warehouse,
                        remarks=f"Inbound transfer from {self.source_warehouse.name} to {self.destination_warehouse.name}"
                    )

        super().save(*args, **kwargs)
