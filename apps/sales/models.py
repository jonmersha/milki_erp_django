from django.utils import timezone
from django.db import models
from django.core.exceptions import ValidationError
from apps.core.base import BaseModel
from apps.inventory.models import Stock, Warehouse
from apps.core.utility.uuidgen import cid, generate_custom_id
from django.db.models import F
from django.db import transaction

# --- Custom Manager for Advanced Business Logic ---

class SalesItemManager(models.Manager):
    def create_sale_item(self, customer, product, warehouse, quantity, price):
        """
        Custom method to:
        1. Find/Create a Pending SalesOrder for the customer.
        2. Check for existing Pending items of the same product to merge.
        3. Validate stock before processing.
        """
        with transaction.atomic():
            # 1. Get or Create a Pending Sales Order for this customer
            sales_order, created = SalesOrder.objects.get_or_create(
                customer=customer,
                order_status='Pending',
                defaults={'payment_status': 'Unpaid'}
            )

            # 2. Validate Stock (Select for update to prevent race conditions)
            try:
                inventory_record = Stock.objects.select_for_update().get(
                    product=product, 
                    warehouse=warehouse
                )
                if inventory_record.quantity < quantity:
                    raise ValidationError(f"Insufficient stock. {inventory_record.quantity} available.")
            except Stock.DoesNotExist:
                raise ValidationError("No inventory record found for this product/warehouse.")

            # 3. Handle Merging: Check if product already exists in this Pending order
            existing_item = self.filter(
                sale_order=sales_order,
                product_name=product,
                status='Pending'
            ).first()

            if existing_item:
                # Update existing item quantity
                existing_item.quantity += quantity
                # Total price is auto-calculated in save()
                existing_item.save()
                return existing_item
            else:
                # Create brand new item
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
            partition = timezone.now().strftime("%Y%m%d")
            self.tracker = generate_custom_id(prefix="CUS", partition=partition, length=16)
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

    def __str__(self):
        return f"Order {self.tracker} - {self.customer.name}"

class SalesItem(models.Model):
    STATUS_CHOICES = [('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')]
    
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
    reg_date = models.DateTimeField(auto_now=True)

    objects = SalesItemManager()  # Register custom manager

    def save(self, *args, **kwargs):
        self.total_price = self.price * self.quantity
        if not self.tracker:
            self.tracker = cid(prefix="SI")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product_name} x {self.quantity} (Order: {self.sale_order.tracker})"

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