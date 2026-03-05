from django.db import models, transaction
from django.dispatch import receiver
from django.dispatch import receiver
from django.forms import ValidationError
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import post_save
from apps.core.base import BaseModel
from apps.core.utility.uuidgen import cid, generate_custom_id
from apps.inventory.models import Product, Stock

# --- Custom Manager for Purchase Logic ---

class PurchaseOrderManager(models.Manager):
    def add_item_to_order(self, supplier, warehouse, product, quantity, unit_price, force_new=False):
        """
        1. Find/Create a Pending PurchaseOrder for the supplier/warehouse.
        2. Merge items if the product already exists in the pending order.
        3. Supports 'force_new' to bypass merging and create a fresh order number.
        """
        with transaction.atomic():
            # 1. Look for existing pending order for this supplier at this warehouse
            purchase_order = None
            if not force_new:
                purchase_order = PurchaseOrder.objects.filter(
                    supplier=supplier,
                    destination_store=warehouse,
                    status='Pending'
                ).first()

            # 2. If no pending order exists (or force_new is True), create a new one
            if not purchase_order:
                purchase_order = PurchaseOrder.objects.create(
                    supplier=supplier,
                    destination_store=warehouse,
                    status='Pending'
                )

            # 3. Check if this product already exists in the found/created order
            # select_for_update() prevents multiple users from updating the same row simultaneously
            existing_item = PurchaseOrderItem.objects.select_for_update().filter(
                purchase_order=purchase_order,
                product=product,
                status='Pending'
            ).first()

            if existing_item:
                # Update quantity and potentially refresh the unit price to the latest
                existing_item.quantity += quantity
                existing_item.unit_price = unit_price
                existing_item.save()
                return existing_item
            else:
                # Create a new line item for this product
                return PurchaseOrderItem.objects.create(
                    purchase_order=purchase_order,
                    product=product,
                    quantity=quantity,
                    unit_price=unit_price,
                    status='Pending'
                )


# --- Purchase Models ---

class Supplier(BaseModel):
    STATUS_CHOICES = [('active', 'Active'), ('inactive', 'Inactive')]
    
    id = models.BigAutoField(primary_key=True)
    tracker = models.CharField(max_length=16, editable=False, unique=True)
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def save(self, *args, **kwargs):
        if not self.tracker:
            self.tracker = generate_custom_id(prefix="SUP", length=16)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class PurchaseOrder(BaseModel):
    STATUS_OPTIONS = [
        ('Pending', 'Pending'), 
        ('Confirmed', 'Confirmed'),
        ('Partially Received', 'Partially Received'),
        ('Completed', 'Completed'), 
        ('Cancelled', 'Cancelled')
    ]
    
    id = models.BigAutoField(primary_key=True)
    tracker = models.CharField(max_length=16, editable=False, unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='purchase_orders')
    destination_store = models.ForeignKey('inventory.Warehouse', on_delete=models.PROTECT)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=25, choices=STATUS_OPTIONS, default='Pending')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, editable=False)

    objects = PurchaseOrderManager() # Link custom manager

    def save(self, *args, **kwargs):
        if not self.tracker:
            self.tracker = cid(prefix="PO", length=16)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"PO {self.tracker} - {self.supplier.name}"

class PurchaseOrderItem(BaseModel):
    STATUS_CHOICES = [('Pending', 'Pending'), ('Received', 'Received'), ('Cancelled', 'Cancelled')]
    
    id = models.BigAutoField(primary_key=True)
    tracker = models.CharField(max_length=16, editable=False, unique=True)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('inventory.Product', on_delete=models.PROTECT)
    
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    line_total = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def save(self, *args, **kwargs):
        # Calculate line total before saving
        self.line_total = self.unit_price * self.quantity
        if not self.tracker:
            self.tracker = cid(prefix="PI")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} ({self.quantity}) - {self.purchase_order.tracker}"

class GRN(BaseModel):
    STATUS_CHOICES = [('Draft', 'Draft'), ('Posted', 'Posted')]

    tracker = models.CharField(max_length=16, editable=False, unique=True)
    purchase_order = models.ForeignKey(
        'PurchaseOrder', 
        on_delete=models.PROTECT, 
        related_name='grns'
    )
    received_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    received_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Draft')
    remarks = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.tracker:
             # Your custom ID generator
            self.tracker = cid(prefix="GRN")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tracker} - {self.purchase_order.tracker}"
class GRNItem(BaseModel):
    STATUS_CHOICES = [('Draft', 'Draft'), ('Posted', 'Posted')]

    grn = models.ForeignKey(GRN, on_delete=models.CASCADE, related_name='items')
    # Link to the specific line on the PO
    purchase_order_item = models.ForeignKey(
        'PurchaseOrderItem', 
        on_delete=models.PROTECT, 
        related_name='grn_lines'
    )
    quantity_received = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Draft')

    def post_to_inventory(self):
        """
        The 'Plain' logic to move goods into stock.
        """
        if self.status == 'Posted':
            return

        with transaction.atomic():
            # 1. Access the Warehouse and Product via the PO link
            warehouse = self.grn.purchase_order.destination_store
            product = self.purchase_order_item.product

            # 2. Update Stock (assuming a Stock model exists)
            from apps.inventory.models import Stock
            stock, _ = Stock.objects.get_or_create(
                warehouse=warehouse,
                product=product,
                defaults={'quantity': 0}
            )
            stock.quantity += self.quantity_received
            stock.save()

            # 3. Mark as Posted
            self.status = 'Posted'
            self.save()

            # 4. Optional: Update the PO Item status to 'Received'
            self._check_po_item_completion()

    def _check_po_item_completion(self):
        po_item = self.purchase_order_item
        # Sum all 'Posted' quantities for this PO line
        total_rec = GRNItem.objects.filter(
            purchase_order_item=po_item, 
            status='Posted'
        ).aggregate(models.Sum('quantity_received'))['quantity_received__sum'] or 0

        if total_rec >= po_item.quantity:
            po_item.status = 'Received'
            po_item.save()