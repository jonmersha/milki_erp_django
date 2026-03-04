# from django.db import models, transaction
# from django.utils import timezone
# from decimal import Decimal
# from apps.core.base import BaseModel
# from apps.core.utility.uuidgen import generate_custom_id, cid
# from apps.inventory.models import InventoryMovementLog, Product, Stock, Warehouse

# # --------------------------------------------------------------------------
# # Managers
# # --------------------------------------------------------------------------

# class PurchaseOrderManager(models.Manager):
#     def add_item_to_order(self, supplier, warehouse, product, quantity, unit_price):
#         """
#         Business Logic:
#         1. Reuse 'pending' PO for this supplier/warehouse or create a new one.
#         2. Merge quantities if product already exists in pending state.
#         """
#         with transaction.atomic():
#             # 1. Get or create the 'Pending' Header
#             purchase_order, created = PurchaseOrder.objects.get_or_create(
#                 supplier=supplier,
#                 destination_store=warehouse,
#                 status='pending',
#             )

#             # 2. Check for existing pending item to merge
#             # select_for_update() prevents multiple requests from overwriting each other
#             existing_item = PurchaseOrderItem.objects.select_for_update().filter(
#                 purchase_order=purchase_order,
#                 product=product,
#                 status='pending'
#             ).first()

#             if existing_item:
#                 existing_item.quantity += int(quantity)
#                 existing_item.unit_price = unit_price
#                 existing_item.save()
#                 return existing_item
#             else:
#                 return PurchaseOrderItem.objects.create(
#                     purchase_order=purchase_order,
#                     product=product,
#                     quantity=quantity,
#                     unit_price=unit_price,
#                     status='pending'
#                 )

# # --------------------------------------------------------------------------
# # Models
# # --------------------------------------------------------------------------

# class Supplier(BaseModel):
#     STATUS_CHOICES = [('active', 'Active'), ('inactive', 'Inactive')]
    
#     id = models.BigAutoField(primary_key=True)
#     tracker = models.CharField(max_length=16, editable=False, unique=True)
#     name = models.CharField(max_length=100)
#     contact_person = models.CharField(max_length=100)
#     phone = models.CharField(max_length=20)
#     email = models.EmailField(max_length=100)
#     address = models.TextField()
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

#     def save(self, *args, **kwargs):
#         if not self.tracker:
#             partition = timezone.now().strftime("%Y%m%d")
#             self.tracker = generate_custom_id(prefix="SUP", partition=partition, length=16)
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.name} ({self.tracker})"


# class PurchaseOrder(BaseModel):
#     STATUS_CHOICES = [('pending', 'Pending'), ('inactive', 'Inactive'), ('received', 'Received')]
    
#     id = models.BigAutoField(primary_key=True)
#     tracker = models.CharField(max_length=16, editable=False, unique=True)
#     destination_store = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='purchase_orders')
#     supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
#     order_date = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
#     # Attach Manager
#     objects = PurchaseOrderManager()

#     def save(self, *args, **kwargs):
#         if not self.tracker:
#             self.tracker = cid(prefix="PO", length=16)
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"PO: {self.tracker} | {self.supplier.name}"


# class PurchaseOrderItem(BaseModel):
#     STATUS_CHOICES = [('pending', 'Pending'), ('received', 'Received')]
    
#     id = models.BigAutoField(primary_key=True)
#     tracker = models.CharField(max_length=16, editable=False, unique=True)
#     purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
#     product = models.ForeignKey(Product, on_delete=models.PROTECT)
#     quantity = models.IntegerField()
#     unit_price = models.DecimalField(max_digits=12, decimal_places=2)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

#     def save(self, *args, **kwargs):
#         if not self.tracker:
#             self.tracker = cid(prefix="POI", length=16)
        
#         super().save(*args, **kwargs)

#         # Automatic Stock Update on "Received" status
#         if self.status == "received":
#             self._update_stock_and_log()

#     def _update_stock_and_log(self):
#         warehouse = self.purchase_order.destination_store
#         with transaction.atomic():
#             stock, _ = Stock.objects.select_for_update().get_or_create(
#                 warehouse=warehouse,
#                 product=self.product,
#                 defaults={"quantity": 0, "unit_price": self.unit_price}
#             )
#             stock.quantity += self.quantity
#             stock.unit_price = self.unit_price
#             stock.save()

#             InventoryMovementLog.objects.create(
#                 product=self.product,
#                 quantity=self.quantity,
#                 movement_type='inbound',
#                 reason='purchase',
#                 destination_warehouse=warehouse,
#                 unit_price=self.unit_price
#             )


# class GoodsReceivingNote(BaseModel):
#     id = models.BigAutoField(primary_key=True)
#     tracker = models.CharField(max_length=16, editable=False, unique=True)
#     purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.PROTECT, related_name='grns')
#     received_by = models.CharField(max_length=100)
#     received_date = models.DateTimeField(default=timezone.now)

#     def save(self, *args, **kwargs):
#         if not self.tracker:
#             self.tracker = cid(prefix="GRN", length=16)
#         super().save(*args, **kwargs)

# class GRNItem(BaseModel):
#     grn = models.ForeignKey(GoodsReceivingNote, on_delete=models.CASCADE, related_name='grn_items')
#     po_item = models.ForeignKey(PurchaseOrderItem, on_delete=models.PROTECT)
#     quantity_received = models.IntegerField()

#     def save(self, *args, **kwargs):
#         with transaction.atomic():
#             # When a GRN Item is saved, mark the original PO Item as received
#             item = self.po_item
#             item.status = 'received'
#             item.quantity = self.quantity_received
#             item.save() # This triggers the stock update logic in PurchaseOrderItem
#             super().save(*args, **kwargs)


from django.db import models, transaction
from django.utils import timezone
from apps.core.base import BaseModel
from apps.core.utility.uuidgen import cid, generate_custom_id

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

class GoodsReceivingNote(BaseModel):
    """Model to track actual receipt of items against a PO"""
    id = models.BigAutoField(primary_key=True)
    tracker = models.CharField(max_length=16, editable=False, unique=True)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.PROTECT, related_name='grns')
    received_date = models.DateTimeField(auto_now_add=True)
    received_by = models.CharField(max_length=100) # Or ForeignKey to User
    remarks = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.tracker:
            self.tracker = cid(prefix="GRN")
        super().save(*args, **kwargs)