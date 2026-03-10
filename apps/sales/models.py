
# from django.db import models, transaction
# from django.core.exceptions import ValidationError
# from django.utils import timezone
# from django.conf import settings
# from apps.core.base import BaseModel
# from apps.core.utility.uuidgen import cid, generate_custom_id
# from apps.inventory.models import Product, Stock, Warehouse

# # --- Custom Manager for Sales Logic ---

# class SalesOrderManager(models.Manager):
#     def add_item_to_order(self, customer, warehouse, product, quantity, price, force_new=False):
#         """
#         1. Find/Create a Pending SalesOrder for the customer.
#         2. Validate Stock availability before allowing the addition.
#         3. Merge items if product exists, or create new.
#         """
#         with transaction.atomic():
#             # 1. Stock Validation (Select for update to lock the row during check)
#             try:
#                 stock_record = Stock.objects.select_for_update().get(
#                     product=product, 
#                     warehouse=warehouse
#                 )
#                 if stock_record.quantity < quantity:
#                     raise ValidationError(f"Insufficient stock. Only {stock_record.quantity} available.")
#             except Stock.DoesNotExist:
#                 raise ValidationError("This product is not stocked in the selected warehouse.")

#             # 2. Get or Create a Pending Sales Order
#             sales_order = None
#             if not force_new:
#                 sales_order = SalesOrder.objects.filter(
#                     customer=customer,
#                     order_status='Pending'
#                 ).first()

#             if not sales_order:
#                 sales_order = SalesOrder.objects.create(
#                     customer=customer,
#                     order_status='Pending'
#                 )

#             # 3. Handle Merging Logic
#             existing_item = SalesItem.objects.select_for_update().filter(
#                 sale_order=sales_order,
#                 product_name=product,
#                 source_whouse=warehouse,
#                 status='Pending'
#             ).first()

#             if existing_item:
#                 existing_item.quantity += quantity
#                 existing_item.price = price
#                 existing_item.save()
#                 return existing_item
#             else:
#                 return SalesItem.objects.create(
#                     sale_order=sales_order,
#                     product_name=product,
#                     source_whouse=warehouse,
#                     inventory=stock_record,
#                     quantity=quantity,
#                     price=price,
#                     status='Pending'
#                 )

# # --- Sales Models ---

# class Customer(BaseModel):
#     STATUS_CHOICES = [('active', 'Active'), ('inactive', 'Inactive')]
    
#     id = models.BigAutoField(primary_key=True)
#     tracker = models.CharField(max_length=16, editable=False, unique=True)
#     name = models.CharField(max_length=100)
#     phone = models.CharField(max_length=20, blank=True, null=True)
#     email = models.EmailField(blank=True, null=True)
#     address = models.TextField(blank=True, null=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

#     def save(self, *args, **kwargs):
#         if not self.tracker:
#             self.tracker = generate_custom_id(prefix="CUS", length=16)
#         super().save(*args, **kwargs)
#     def __str__(self):
#         # This returns the name instead of "Customer object (1)"
#         return f"{self.name} ({self.tracker})"

# class SalesOrder(BaseModel):
#     ORDER_OPTIONS = [
#         ('Pending', 'Pending'), ('Confirmed', 'Confirmed'),
#         ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'),
#     ]
#     PAYMENT_OPTIONS = [('Unpaid', 'Unpaid'), ('Paid', 'Paid'), ('Refunded', 'Refunded')]
    
#     id = models.BigAutoField(primary_key=True)
#     tracker = models.CharField(max_length=16, editable=False, unique=True)
#     customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='sales_orders')
#     order_status = models.CharField(max_length=20, choices=ORDER_OPTIONS, default='Pending')
#     payment_status = models.CharField(max_length=20, choices=PAYMENT_OPTIONS, default='Unpaid')
#     order_date = models.DateTimeField(auto_now_add=True)

#     objects = SalesOrderManager()

#     def save(self, *args, **kwargs):
#         if not self.tracker:
#             self.tracker = cid(prefix="SO", length=16)
#         super().save(*args, **kwargs)

# class SalesItem(BaseModel):
#     STATUS_CHOICES = [('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')]
    
#     id = models.BigAutoField(primary_key=True)
#     tracker = models.CharField(max_length=16, editable=False, unique=True)
#     sale_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name='items')
#     product_name = models.ForeignKey('inventory.Product', on_delete=models.PROTECT)
#     source_whouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
#     inventory = models.ForeignKey(Stock, on_delete=models.PROTECT) # Direct link to stock row
    
#     quantity = models.PositiveIntegerField()
#     price = models.DecimalField(max_digits=12, decimal_places=2)
#     total_price = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

#     def save(self, *args, **kwargs):
#         self.total_price = self.price * self.quantity
#         if not self.tracker:
#             self.tracker = cid(prefix="SI")
#         super().save(*args, **kwargs)

#     def deduct_from_inventory(self):
#         """
#         Equivalent to the GRNItem 'post_to_inventory' logic, 
#         but subtracts stock when the order is Confirmed/Shipped.
#         """
#         if self.status != 'Pending':
#             return

#         with transaction.atomic():
#             stock = self.inventory
#             if stock.quantity < self.quantity:
#                 raise ValidationError(f"Insufficient stock for {self.product_name}")
            
#             stock.quantity -= self.quantity
#             stock.save()
            
#             self.status = 'Confirmed'
#             self.save()

# class SalesTransaction(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     tracker = models.CharField(max_length=16, editable=False, unique=True)
#     sale_item = models.ForeignKey(SalesItem, on_delete=models.CASCADE, related_name='transactions')
#     transaction_date = models.DateTimeField(auto_now_add=True)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     payment_method = models.CharField(max_length=50)
#     bank_reference = models.CharField(max_length=100, blank=True, null=True)
#     payment_status = models.CharField(max_length=20, default='Unpaid')

#     def save(self, *args, **kwargs):
#         if not self.tracker:
#             self.tracker = cid(prefix="ST")
#         super().save(*args, **kwargs)


from django.utils import timezone
from django.db import models, transaction
from django.core.exceptions import ValidationError
from apps.core.base import BaseModel
from apps.inventory.models import Stock, Warehouse
from apps.core.utility.uuidgen import cid, generate_custom_id

# --- Custom Manager for Advanced Business Logic ---

# class SalesItemManager(models.Manager):
#     def create_sale_item(self, customer, product, warehouse, quantity, price):
#         """
#         1. Find/Create a Pending SalesOrder.
#         2. Validate & LOCK Stock immediately (Hard Lock).
#         3. Merge or Create Item and update Stock balance.
#         """
#         with transaction.atomic():
#             # 1. Get/Create Pending Sales Order
#             sales_order, _ = SalesOrder.objects.get_or_create(
#                 customer=customer,
#                 order_status='Pending',
#                 defaults={'payment_status': 'Unpaid'}
#             )

#             # 2. Validate and Lock Stock row
#             try:
#                 inventory_record = Stock.objects.select_for_update().get(
#                     product=product, 
#                     warehouse=warehouse
#                 )
#                 if inventory_record.quantity < quantity:
#                     raise ValidationError(f"Insufficient stock. {inventory_record.quantity} available.")
#             except Stock.DoesNotExist:
#                 raise ValidationError("No inventory record found for this product/warehouse.")

#             # 3. Handle Stock Deduction (The "Lock")
#             inventory_record.quantity -= quantity
#             inventory_record.save()

#             # 4. Handle Merging
#             existing_item = self.filter(
#                 sale_order=sales_order,
#                 product_name=product,
#                 status='Pending'
#             ).first()

#             if existing_item:
#                 existing_item.quantity += quantity
#                 existing_item.save()
#                 return existing_item
#             else:
#                 return self.create(
#                     sale_order=sales_order,
#                     product_name=product,
#                     source_whouse=warehouse,
#                     inventory=inventory_record,
#                     quantity=quantity,
#                     price=price,
#                     status='Pending'
#                 )
class SalesItemManager(models.Manager):
    def create_sale_item(self, customer, product, warehouse, quantity, price):
        with transaction.atomic():
            # 1. Get/Create Order
            sales_order, _ = SalesOrder.objects.get_or_create(
                customer=customer,
                order_status='Pending',
                defaults={'payment_status': 'Unpaid'}
            )

            # 2. Lock Stock Row and Update BOTH fields
            try:
                inventory_record = Stock.objects.select_for_update().get(
                    product=product, 
                    warehouse=warehouse
                )
                if inventory_record.quantity < quantity:
                    raise ValidationError(f"Insufficient stock. {inventory_record.quantity} available.")
                
                # --- THE FIX: Balancing the fields ---
                inventory_record.quantity -= quantity       # Deduct from available
                inventory_record.locked_amount += quantity   # Add to locked/reserved
                inventory_record.save()

            except Stock.DoesNotExist:
                raise ValidationError("No inventory record found.")

            # 3. Merging logic
            existing_item = self.filter(
                sale_order=sales_order,
                product_name=product,
                status='Pending'
            ).first()

            if existing_item:
                existing_item.quantity += quantity
                existing_item.save()
                return existing_item
            else:
                return self.create(
                    sale_order=sales_order,
                    product_name=product,
                    source_whouse=warehouse,
                    inventory=inventory_record,
                    quantity=quantity,
                    price=price,
                    status='Pending'
                )
# --- Models ---

class Customer(BaseModel):
    STATUS_CHOICES = [('active', 'Active'), ('inactive', 'Inactive')]
    id = models.BigAutoField(primary_key=True)
    tracker = models.CharField(max_length=16, editable=False, unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def save(self, *args, **kwargs):
        if not self.tracker:
            self.tracker = generate_custom_id(prefix="CUS", length=16)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.tracker})"

class SalesOrder(models.Model):
    ORDER_OPTIONS = [
        ('Pending', 'Pending'), ('Confirmed', 'Confirmed'),
        ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'),
    ]
    PAYMENT_OPTIONS = [('Unpaid', 'Unpaid'), ('Paid', 'Paid'), ('Refunded', 'Refunded')]
    
    id = models.BigAutoField(primary_key=True)
    tracker = models.CharField(max_length=16, editable=False, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='sales_orders')
    order_status = models.CharField(max_length=20, choices=ORDER_OPTIONS, default='Pending')
    order_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_OPTIONS, default='Unpaid')

    def save(self, *args, **kwargs):
        if not self.tracker:
            self.tracker = cid(prefix="SO", length=16)
        super().save(*args, **kwargs)

class SalesItem(models.Model):
    STATUS_CHOICES = [('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')]
    
    id = models.BigAutoField(primary_key=True)
    tracker = models.CharField(max_length=16, editable=False, unique=True)
    sale_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name='items')
    product_name = models.ForeignKey('inventory.Product', on_delete=models.PROTECT)
    source_whouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
    inventory = models.ForeignKey(Stock, on_delete=models.PROTECT)
    
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    status = models.CharField(default='Pending', max_length=20, choices=STATUS_CHOICES)

    objects = SalesItemManager()

    def save(self, *args, **kwargs):
        self.total_price = self.price * self.quantity
        if not self.tracker:
            self.tracker = cid(prefix="SI")
        super().save(*args, **kwargs)

    # def delete(self, *args, **kwargs):
    #     """IMPORTANT: Return stock balance when item is removed from order."""
    #     with transaction.atomic():
    #         stock = self.inventory
    #         stock.quantity += self.quantity
    #         stock.save()
    #         super().delete(*args, **kwargs)
    def delete(self, *args, **kwargs):
            with transaction.atomic():
                stock = self.inventory
                # Reverse the lock logic
                stock.quantity += self.quantity         # Return to available
                stock.locked_amount -= self.quantity     # Remove from locked
                stock.save()
                super().delete(*args, **kwargs)
class SalesTransaction(models.Model):
    id = models.BigAutoField(primary_key=True)
    tracker = models.CharField(max_length=16, editable=False, unique=True)
    sale_item = models.ForeignKey(SalesItem, on_delete=models.CASCADE, related_name='transactions')
    transaction_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    bank_reference = models.CharField(max_length=100, blank=True, null=True)
    payment_status = models.CharField(max_length=20, default='Unpaid')

    def save(self, *args, **kwargs):
        if not self.tracker:
            self.tracker = cid(prefix="ST")
        super().save(*args, **kwargs)