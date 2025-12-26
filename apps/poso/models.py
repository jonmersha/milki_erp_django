# # pos/models.py

# import uuid
# from django.db import models,transaction


# from decimal import Decimal

# from core.base import BaseModel
# from inventory.models import InventoryMovementLog, Product, Stock, Warehouse
# from django.utils import timezone
# from core.utility.uuidgen import generate_custom_id
# from django.core.exceptions import ValidationError

# # -----------------------------
# # Partners: Supplier & Customer
# # -----------------------------
# # class Supplier(BaseModel):
# #     STATUS_CHOICES = [
# #         ('active', 'Active'),
# #         ('inactive', 'Inactive'),
# #     ]
# #     id = models.CharField(
# #         max_length=16,
# #         primary_key=True,
# #         editable=False,
# #         unique=True
# #     )
# #     name = models.CharField(max_length=100)
# #     contact_person = models.CharField(max_length=100)
# #     phone = models.CharField(max_length=20)
# #     email = models.CharField(max_length=100)
# #     address = models.TextField()
# #     status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True, null=True)
# #     def save(self, *args, **kwargs):
# #         if not self.id:
# #             partition = timezone.now().strftime("%Y%m%d")
# #             self.id = generate_custom_id(prefix="SUP", partition=partition, length=16)
# #         super().save(*args, **kwargs)


# #     def __str__(self):
# #         return self.name


# # class Customer(BaseModel):
# #     STATUS_CHOICES = [
# #         ('active', 'Active'),
# #         ('inactive', 'Inactive'),
# #     ]
# #     id = models.CharField(
# #         max_length=16,
# #         primary_key=True,
# #         editable=False,
# #         unique=True
# #     )
# #     name = models.CharField(max_length=100)
# #     phone = models.CharField(max_length=20, blank=True, null=True)
# #     email = models.CharField(max_length=100, blank=True, null=True)
# #     address = models.TextField(blank=True, null=True)
# #     status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True, null=True)
# #     def save(self, *args, **kwargs):
# #         if not self.id:
# #             partition = timezone.now().strftime("%Y%m%d")
# #             self.id = generate_custom_id(prefix="CUS", partition=partition, length=16)
# #         super().save(*args, **kwargs)


# #     def __str__(self):
# #         return self.name

# # -----------------------------
# # Purchase Orders (PO + POI)
# # -----------------------------
# # class PurchaseOrder(BaseModel):
# #     STATUS_CHOICES = [
# #         ('pending', 'Pending'),
# #         ('inactive', 'Inactive'),
# #         ('received','Received')
# #     ]
# #     id = models.CharField(
# #         max_length=16,
# #         primary_key=True,
# #         editable=False,
# #         unique=True
# #     )
# #     destination_store = models.ForeignKey(
# #         Warehouse,
# #         on_delete=models.PROTECT,
# #         related_name='purchase_orders'
# #     )
# #     supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
# #     order_date = models.DateTimeField(auto_now_add=True)
# #     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
# #     def save(self, *args, **kwargs):
# #         if not self.id:
# #             partition = timezone.now().strftime("%Y%m%d")
# #             self.id = generate_custom_id(prefix="PO", partition=partition, length=16)
# #         super().save(*args, **kwargs)

# #     def __str__(self):
# #         return f"PO-{self.id}"
    
# #----------------------------------------------
# #purchase order items
# #------------------------------------------------------



# # class SalesOrder(BaseModel):
# #     STATUS_CHOICES = [
# #         ('draft','Draft'),
# #         ('pending', 'Pending'),
# #         ('approved', 'Approved'),
# #         ('rejected', 'Rejected'),
# #         ('completed', 'Completed'),
# #         ('received','Received')
# #         ]
# #     id = models.CharField(
# #         max_length=16,
# #         primary_key=True,
# #         editable=False,
# #         unique=True
# #     )
# #     source_store = models.ForeignKey(
# #         Warehouse,
# #         on_delete=models.PROTECT,
# #         related_name='sales_orders'
# #     )
# #     customer = models.ForeignKey(Customer, on_delete=models.PROTECT, null=True, blank=True)
# #     order_date = models.DateTimeField(auto_now_add=True)
# #     status = models.CharField(max_length=20, choices=STATUS_CHOICES,default='draft')
# #     def save(self, *args, **kwargs):
# #         if not self.id:
# #             partition = timezone.now().strftime("%Y%m%d")
# #             self.id = generate_custom_id(prefix="SO", partition=partition, length=16)
# #         super().save(*args, **kwargs)


# #     def __str__(self):
# #         return f"SO-{self.id}"

# #-----------------------------

        
# # class SalesOrderItem(BaseModel):
# #     id = models.CharField(
# #         max_length=16,
# #         primary_key=True,
# #         editable=False,
# #         unique=True
# #     )
# #     sales_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name='items')
# #     product = models.ForeignKey(Product, on_delete=models.PROTECT)
# #     quantity = models.IntegerField()
# #     unit_price = models.DecimalField(max_digits=12, decimal_places=2)

# #     def save(self, *args, **kwargs):
# #         if not self.id:
# #             partition = timezone.now().strftime("%Y%m%d")
# #             self.id = generate_custom_id(prefix="SOI", partition=partition, length=16)
# #         super().save(*args, **kwargs)


# #     @property
# #     def total_price(self):
# #         return self.quantity * self.unit_price
# #     class Meta:
# #         constraints = [
# #             models.UniqueConstraint(fields=['sales_order', 'product'], name='unique_product_per_SO')
# #         ]

# # class SalesOrderItem(BaseModel):
# #     STATUS_CHOICES = [
# #         ('pending', 'Pending'),
# #         ('dispatched', 'Dispatched'),
# #         ('delivered', 'Delivered'),
# #     ]

# #     id = models.CharField(
# #         max_length=16,
# #         primary_key=True,
# #         editable=False,
# #         unique=True
# #     )
# #     sales_order = models.ForeignKey(
# #         SalesOrder,
# #         on_delete=models.CASCADE,
# #         related_name='items'
# #     )
# #     product = models.ForeignKey(Product, on_delete=models.PROTECT)
# #     quantity = models.IntegerField()
# #     unit_price = models.DecimalField(max_digits=12, decimal_places=2)
# #     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

# #     def save(self, *args, **kwargs):
# #         from decimal import Decimal
# #         with transaction.atomic():
# #             # --- Generate ID if new ---
# #             if not self.id:
# #                 partition = timezone.now().strftime("%Y%m%d")
# #                 self.id = generate_custom_id(prefix="SOI", partition=partition, length=16)

# #             self.quantity = int(self.quantity)
# #             self.unit_price = Decimal(self.unit_price)

# #             # --- Check if duplicate item exists ---
# #             duplicate = SalesOrderItem.objects.select_for_update().filter(
# #                 sales_order=self.sales_order,
# #                 product=self.product
# #             ).exclude(pk=self.pk).first()

# #             if duplicate and duplicate.status == "pending":
# #                 # Merge quantities and keep updated price
# #                 duplicate.quantity += self.quantity
# #                 duplicate.unit_price = self.unit_price
# #                 if self.status in ["dispatched", "delivered"]:
# #                     duplicate.status = self.status
# #                     self._update_stock_and_log(duplicate)
# #                 duplicate.save(update_fields=['quantity', 'unit_price', 'status'])
# #                 return

# #             # --- Save normally (new or existing non-pending) ---
# #             super().save(*args, **kwargs)

# #             if self.status in ["dispatched", "delivered"]:
# #                 self._update_stock_and_log(self)

# #     def _update_stock_and_log(self, item):
# #         """Reduce stock and log outbound movement for a completed sale."""
# #         warehouse = item.sales_order.source_store
# #         stock = Stock.objects.select_for_update().filter(
# #             warehouse=warehouse,
# #             product=item.product
# #         ).first()

# #         if not stock:
# #             raise ValueError(f"Stock for {item.product.name} not found in warehouse {warehouse.name}")

# #         if stock.quantity < item.quantity:
# #             raise ValueError(f"Insufficient stock for {item.product.name}. Available: {stock.quantity}")

# #         # --- Deduct stock ---
# #         stock.quantity -= item.quantity
# #         stock.total_value = stock.quantity * stock.unit_price
# #         stock.remarks = f"Dispatched via SO {item.sales_order.id}"
# #         stock.save(update_fields=['quantity', 'total_value', 'remarks'])

# #         # --- Log inventory movement ---
# #         InventoryMovementLog.objects.create(
# #             product=item.product,
# #             quantity=item.quantity,
# #             movement_type='outbound',
# #             reason='sales',
# #             source_warehouse=warehouse,
# #             unit_price=item.unit_price,
# #             remarks=f"Dispatched via SO {item.sales_order.id}"
# #         )

# #     @property
# #     def total_price(self):
# #         return self.quantity * self.unit_price

# #     @property
# #     def warehouse_info(self):
# #         warehouse = self.sales_order.source_store
# #         return {
# #             "id": warehouse.id,
# #             "name": warehouse.name,
# #             "code": getattr(warehouse, "code", None),
# #             "address": getattr(warehouse, "address", None)
# #         }

# #     class Meta:
# #         constraints = [
# #             models.UniqueConstraint(fields=['sales_order', 'product'], name='unique_product_per_SO')
# #         ]

# # class SalesOrderItem(BaseModel):
# #     STATUS_CHOICES = [
# #         ('PENDING', 'Pending'),
# #         ('CONFIRMED', 'Confirmed'),
# #         ('DELIVERED', 'Delivered'),
# #         ('CANCELLED', 'Cancelled'),
# #     ]

# #     id = models.CharField(max_length=16, primary_key=True, editable=False, unique=True)
# #     sales_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name='items')
# #     product = models.ForeignKey(Product, on_delete=models.PROTECT)
# #     quantity = models.PositiveIntegerField()
# #     unit_price = models.DecimalField(max_digits=12, decimal_places=2)
# #     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
# #     remarks = models.TextField(blank=True, null=True)

# #     class Meta:
# #         constraints = [
# #             models.UniqueConstraint(fields=['sales_order', 'product'], name='unique_product_per_SO')
# #         ]

# #     def save(self, *args, **kwargs):
# #         if not self.id:
# #             partition = timezone.now().strftime("%Y%m%d")
# #             self.id = generate_custom_id(prefix="SOI", partition=partition, length=16)

# #         with transaction.atomic():
# #             is_new = self._state.adding
# #             source_warehouse = self.sales_order.source_store
# #             stock = Stock.objects.select_for_update().filter(
# #                 warehouse=source_warehouse, product=self.product
# #             ).first()

# #             if not stock:
# #                 raise ValidationError("No stock record found for this product in the selected warehouse.")

# #             # --- Initial creation ---
# #             if is_new:
# #                 if stock.quantity < self.quantity:
# #                     raise ValidationError("Insufficient stock to fulfill this order.")
# #                 # Lock stock (reserve for this sale)
# #                 stock.quantity -= self.quantity
# #                 stock.locked_amount += self.quantity
# #                 stock.save(update_fields=["quantity", "locked_amount"])

# #             else:
# #                 prev = SalesOrderItem.objects.select_for_update().get(pk=self.pk)

# #                 # Prevent changes once fully delivered
# #                 if prev.status in ["DELIVERED"]:
# #                     raise ValidationError("Cannot modify a delivered item.")

# #                 # Handle cancellation
# #                 if self.status == "CANCELLED" and prev.status != "CANCELLED" and prev.status != "DELIVERED":
# #                     stock.quantity += prev.quantity
# #                     stock.locked_amount -= prev.quantity
# #                     stock.save(update_fields=["quantity", "locked_amount"])

# #                 # # Handle dispatch
# #                 # elif self.status == "DISPATCHED":
# #                 #     stock.locked_amount -= self.quantity
# #                 #     stock.save(update_fields=["locked_amount"])

# #                 #     InventoryMovementLog.objects.create(
# #                 #         product=self.product,
# #                 #         quantity=self.quantity,
# #                 #         movement_type='outbound',
# #                 #         reason='sales',
# #                 #         source_warehouse=source_warehouse,
# #                 #         remarks=f"Dispatched via Sales Order {self.sales_order.id}"
# #                 #     )

# #                 # Handle delivery (final stage) add to stock movement log

# #                 elif self.status == "DELIVERED":
# #                     stock.locked_amount -= self.quantity
# #                     stock.remarks = f"Delivered via Sales Order {self.sales_order.id} of quantity : {self.quantity}"
# #                     stock.save(update_fields=["locked_amount"])

# #                     InventoryMovementLog.objects.create(
# #                         product=self.product,
# #                         quantity=self.quantity,
# #                         movement_type='outbound',
# #                         reason='sales',
# #                         source_warehouse=source_warehouse,
# #                         remarks=f"Delivered via Sales Order {self.sales_order.id}"
# #                     )

# #             super().save(*args, **kwargs)

# #     @property
# #     def total_price(self):
# #         return self.quantity * self.unit_price

# # class SalesOrderItem(BaseModel):
# #     STATUS_CHOICES = [
# #         ('PENDING', 'Pending'),
# #         ('CONFIRMED', 'Confirmed'),
# #         ('DELIVERED', 'Delivered'),
# #         ('CANCELLED', 'Cancelled'),
# #     ]

# #     id = models.CharField(max_length=16, primary_key=True, editable=False)
# #     sales_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name='items')
# #     product = models.ForeignKey(Product, on_delete=models.PROTECT)
# #     quantity = models.PositiveIntegerField()
# #     unit_price = models.DecimalField(max_digits=12, decimal_places=2)
# #     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
# #     remarks = models.TextField(blank=True, null=True)

# #     class Meta:
# #         indexes = [models.Index(fields=['sales_order', 'product'])]

# #     def clean(self):
# #         """Basic validation before saving."""
# #         if self._state.adding and self.status != 'PENDING':
# #             raise ValidationError("New Sales Order Items must start with PENDING status.")

# #         if self.quantity <= 0:
# #             raise ValidationError("Quantity must be greater than zero.")

# #     def adjust_stock(self, delta_locked=0, delta_qty=0, remarks=None):
# #         """Utility to safely update stock quantities."""
# #         stock = Stock.objects.select_for_update().filter(
# #             warehouse=self.sales_order.source_store,
# #             product=self.product
# #         ).first()
# #         if not stock:
# #             raise ValidationError("No stock record found for this product in the selected warehouse.")

# #         if delta_qty < 0 and stock.quantity < abs(delta_qty):
# #             raise ValidationError("Insufficient stock to fulfill this order.")

# #         stock.quantity += delta_qty
# #         stock.locked_amount += delta_locked
# #         if remarks:
# #             stock.remarks = remarks
# #         stock.save(update_fields=["quantity", "locked_amount", "remarks"])

# #     def process_delivery(self):
# #         """Handle delivery transition."""
# #         self.adjust_stock(delta_locked=-self.quantity,
# #                           remarks=f"Delivered via Sales Order {self.sales_order.id}, qty {self.quantity}")

# #         InventoryMovementLog.objects.create(
# #             product=self.product,
# #             quantity=self.quantity,
# #             movement_type='outbound',
# #             reason='sales',
# #             source_warehouse=self.sales_order.source_store,
# #             remarks=f"Delivered via Sales Order {self.sales_order.id}"
# #         )

# #     def process_cancellation(self):
# #         """Handle cancellation."""
# #         self.adjust_stock(delta_locked=-self.quantity, delta_qty=+self.quantity)
# #         self.status = "CANCELLED"

# #     def save(self, *args, **kwargs):
# #         if not self.id:
# #             partition = timezone.now().strftime("%Y%m%d")
# #             self.id = generate_custom_id(prefix="SOI", partition=partition, length=16)

# #         with transaction.atomic():
# #             is_new = self._state.adding
# #             self.clean()

# #             if is_new:
# #                 self.adjust_stock(delta_locked=+self.quantity, delta_qty=-self.quantity)
# #             else:
# #                 prev = SalesOrderItem.objects.select_for_update().get(pk=self.pk)

# #                 if prev.status == "DELIVERED":
# #                     raise ValidationError("Delivered items cannot be modified.")

# #                 if self.status == "DELIVERED" and prev.status != "DELIVERED":
# #                     self.process_delivery()

# #                 elif self.status == "CANCELLED" and prev.status != "CANCELLED":
# #                     self.process_cancellation()

# #             super().save(*args, **kwargs)

# #     @property
# #     def total_price(self):
# #         return self.quantity * self.unit_price


# # -----------------------------
# # Payments
# # -----------------------------
# # class Payment(BaseModel):
# #     id = models.CharField(
# #         max_length=16,
# #         primary_key=True,
# #         editable=False,
# #         unique=True
# #     )
# #     sales_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, null=True, blank=True)
# #     purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, null=True, blank=True)
# #     amount = models.DecimalField(max_digits=14, decimal_places=2)
# #     method = models.CharField(max_length=50, choices=[('cash','Cash'), ('card','Card'), ('online','Online')])
# #     status = models.CharField(max_length=20, choices=[('pending','Pending'), ('paid','Paid')])
# #     def save(self, *args, **kwargs):
# #         if not self.id:
# #             partition = timezone.now().strftime("%Y%m%d")
# #             self.id = generate_custom_id(prefix="PYT", partition=partition, length=16)
# #         super().save(*args, **kwargs)


# #     def __str__(self):
# #         if self.sales_order:
# #             return f"Payment-SO-{self.sales_order.id}"
# #         if self.purchase_order:
# #             return f"Payment-PO-{self.purchase_order.id}"


# # -----------------------------
# # Invoices
# # -----------------------------
# # class Invoice(BaseModel):
# #     id = models.CharField(
# #         max_length=16,
# #         primary_key=True,
# #         editable=False,
# #         unique=True
# #     )
# #     sales_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, null=True, blank=True)
# #     purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, null=True, blank=True)
# #     invoice_date = models.DateTimeField(auto_now_add=True)
# #     total_amount = models.DecimalField(max_digits=14, decimal_places=2)
# #     status = models.CharField(max_length=20, choices=[('draft','Draft'), ('sent','Sent'), ('paid','Paid')])
# #     def save(self, *args, **kwargs):
# #         if not self.id:
# #             partition = timezone.now().strftime("%Y%m%d")
# #             self.id = generate_custom_id(prefix="INV", partition=partition, length=16)
# #         super().save(*args, **kwargs)

# #     def __str__(self):
# #         return f"Invoice-{self.id}"



# # class PurchaseOrderItem(BaseModel):
# #     STATUS_CHOICES = [
# #         ('pending', 'Pending'),
# #         ('received', 'Received'),
# #     ]

# #     id = models.CharField(
# #         max_length=16,
# #         primary_key=True,
# #         editable=False,
# #         unique=True
# #     )
# #     purchase_order = models.ForeignKey(
# #         PurchaseOrder,
# #         on_delete=models.CASCADE,
# #         related_name='items'
# #     )
# #     product = models.ForeignKey(Product, on_delete=models.PROTECT)
# #     quantity = models.IntegerField()
# #     unit_price = models.DecimalField(max_digits=12, decimal_places=2)
# #     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

# #     def save(self, *args, **kwargs):
# #         with transaction.atomic():
# #             # --- Generate ID if new ---
# #             if not self.id:
# #                 partition = timezone.now().strftime("%Y%m%d")
# #                 self.id = generate_custom_id(prefix="POI", partition=partition, length=16)

# #             # --- Ensure proper types ---
# #             self.quantity = int(self.quantity)
# #             self.unit_price = Decimal(self.unit_price)

# #             # --- Handle duplicates manually ---
# #             duplicate = PurchaseOrderItem.objects.select_for_update().filter(
# #                 purchase_order=self.purchase_order,
# #                 product=self.product
# #             ).exclude(pk=self.pk).first()

# #             if duplicate and duplicate.status == "pending":
# #                 # Merge quantities and update unit price
# #                 duplicate.quantity += self.quantity
# #                 duplicate.unit_price = self.unit_price
# #                 if self.status == "received":
# #                     duplicate.status = "received"
# #                     self._update_stock_and_log(duplicate)
# #                 duplicate.save(update_fields=['quantity', 'unit_price', 'status'])
# #                 return  # Exit without creating new row

# #             # --- Save normally (new or received duplicate) ---
# #             super().save(*args, **kwargs)

# #             if self.status == "received":
# #                 self._update_stock_and_log(self)

# #     def _update_stock_and_log(self, item):
# #         warehouse = item.purchase_order.destination_store
# #         stock, _ = Stock.objects.select_for_update().get_or_create(
# #             warehouse=warehouse,
# #             product=item.product,
# #             defaults={
# #                 "quantity": 0,
# #                 "locked_amount": 0,
# #                 "unit_price": Decimal(item.unit_price),
# #                 "total_value": 0,
# #                 "remarks": f"Created via PO {item.purchase_order.id}"
# #             }
# #         )

# #         stock.quantity += item.quantity
# #         stock.unit_price = Decimal(item.unit_price)
# #         stock.total_value = stock.quantity * stock.unit_price
# #         stock.remarks = f"Updated via PO {item.purchase_order.id}"
# #         stock.save(update_fields=['quantity', 'unit_price', 'total_value', 'remarks'])

# #         InventoryMovementLog.objects.create(
# #             product=item.product,
# #             quantity=item.quantity,
# #             movement_type='inbound',
# #             reason='purchase',
# #             destination_warehouse=warehouse,
# #             unit_price=item.unit_price,
# #             remarks=f"Received from PO {item.purchase_order.id}"
# #         )

# #     @property
# #     def total_price(self):
# #         return Decimal(self.quantity) * Decimal(self.unit_price)

# #     @property
# #     def warehouse_info(self):
# #         warehouse = self.purchase_order.destination_store
# #         return {
# #             "id": warehouse.id,
# #             "name": warehouse.name,
# #             "code": getattr(warehouse, "code", None),
# #             "address": getattr(warehouse, "address", None)
# #         }