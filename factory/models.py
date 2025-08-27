from django.db import models, transaction
from django.conf import settings
from django.utils import timezone
from django.contrib import admin


#customer
class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name

    class Meta:
        ordering = ['user__first_name', 'user__last_name']
        permissions = [
            ('view_history', 'Can view history')
        ]


# 2. Company
class Company(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,related_name="company_customer")
    logo_url = models.TextField(blank=True, null=True)
    company_status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# 3. Factory
class Factory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    location_name = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    admin_region = models.CharField(max_length=100, blank=True, null=True)
    latitude_point = models.CharField(max_length=100, blank=True, null=True)
    longitude_point = models.CharField(max_length=100, blank=True, null=True)
    is_operational = models.BooleanField(default=False)
    production_capacity = models.IntegerField(blank=True, null=True)
    is_authorized = models.BooleanField(default=False)
    authorization_time = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    inputer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, related_name="factory_inputer")
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# 4. Warehouse
class Warehouse(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
    ]

    capacity = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True, null=True)
    is_authorized = models.BooleanField(default=False)
    authorization_time = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    authorized_by = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    factory = models.ForeignKey(Factory, on_delete=models.CASCADE)

    def __str__(self):
        return f"Warehouse {self.id} - {self.factory.name}"


# 5. Category
class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


# 6. Product
class Product(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
    ]

    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name="product_category")
    unit_of_measure = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True, null=True)
    is_authorized = models.BooleanField(default=False)
    authorization_time = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    authorizer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, related_name="product_authorizer")
    inputer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="product_inputer")

    def __str__(self):
        return self.name


# 7. Stock
class Stock(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    quantity = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    is_authorized = models.BooleanField(default=False)
    authorization_time = models.DateTimeField(blank=True, null=True)
    authorizer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="stock_authorizer")
    inputer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="stock_inputer")

    def __str__(self):
        return f"{self.product.name} in {self.warehouse}"


# 8. Stock Movement Log
class StockMovementLog(models.Model):
    MOVEMENT_CHOICES = [
        ('PURCHASE', 'Purchase'),
        ('SALES', 'Sales'),
        ('TRANSFER', 'Transfer'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    mdate = models.DateTimeField(default=timezone.now)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    quantity = models.IntegerField()
    movement_type = models.CharField(max_length=10, choices=MOVEMENT_CHOICES)
    remarks = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    is_authorized = models.BooleanField(default=False)
    authorization_time = models.DateTimeField(blank=True, null=True)
    logged_at = models.DateTimeField(default=timezone.now)
    source_factory = models.ForeignKey(Factory, on_delete=models.CASCADE, related_name="source_factory")
    destination_factory = models.ForeignKey(Factory, on_delete=models.CASCADE, related_name="destination_factory")
    source_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="source_warehouse")
    destination_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="destination_warehouse")
    authorizer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, related_name="movement_authorizer")
    inputer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, related_name="movement_inputer")

    def __str__(self):
        return f"{self.movement_type} - {self.product.name}"
# 9. Suppliers
class Supplier(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
    ]

    supplier_name = models.CharField(max_length=100)
    supplier_contact_person = models.CharField(max_length=100, blank=True, null=True)
    supplier_phone = models.CharField(max_length=20, blank=True, null=True)
    supplier_email = models.CharField(max_length=100, blank=True, null=True)
    supplier_address = models.TextField(blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    supplier_status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True, null=True)
    is_authorized = models.BooleanField(default=False)
    authorization_time = models.DateTimeField(blank=True, null=True)
    inputer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="supplier_inputer")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.supplier_name


# 10. Purchase Order
class PurchaseOrder(models.Model):
    ORDER_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('PAID', 'Paid'),
        ('UNPAID', 'Unpaid'),
        ('PARTIAL', 'Partial'),
    ]

    placed_at = models.DateTimeField(default=timezone.now)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    inputer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="purchase_order_inputer")
    authorizer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="purchase_order_authorizer")
    order_status = models.CharField(max_length=30, choices=ORDER_STATUS_CHOICES, blank=True, null=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, blank=True, null=True)
    is_authorized = models.BooleanField(default=False)
    authorized_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"PO-{self.id} - {self.supplier.supplier_name}"


# 11. Purchase Order Item
class PurchaseOrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    factory = models.ForeignKey(Factory, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, blank=True, null=True)
    order_date = models.DateTimeField(blank=True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    payment_status = models.CharField(max_length=20, blank=True, null=True)
    authorization_time = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name="items")

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


# 12. Sales Order
class SalesOrder(models.Model):
    ORDER_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('PAID', 'Paid'),
        ('UNPAID', 'Unpaid'),
        ('PARTIAL', 'Partial'),
    ]

    placed_at = models.DateTimeField(default=timezone.now)
    to_customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    inputer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, related_name="sales_order_inputer")
    authorizer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, related_name="sales_order_authorizer")
    order_status = models.CharField(max_length=30, choices=ORDER_STATUS_CHOICES, blank=True, null=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, blank=True, null=True)
    is_authorized = models.BooleanField(default=False)
    authorization_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"SO-{self.id} to {self.to_customer}"


# 13. Sales Order Item
class SalesOrderItem(models.Model):
    sales_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    factory = models.ForeignKey(Factory, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, blank=True, null=True)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    total_price = models.DecimalField(max_digits=14, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


# 14. Invoice
class Invoice(models.Model):
    INVOICE_TYPE_CHOICES = [
        ('SALES', 'Sales'),
        ('PURCHASE', 'Purchase'),
    ]

    invoice_number = models.CharField(max_length=50, unique=True)
    invoice_type = models.CharField(max_length=10, choices=INVOICE_TYPE_CHOICES)
    sales_order = models.ForeignKey(SalesOrder, on_delete=models.SET_NULL, blank=True, null=True)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.SET_NULL, blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, blank=True, null=True)
    issue_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.invoice_number


# 15. Invoice Item
class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    total_price = models.DecimalField(max_digits=14, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


# 16. Payment Method
class PaymentMethod(models.Model):
    method_name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.method_name


# 17. Payment
class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    payer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, related_name="payments_made")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, blank=True, null=True, related_name="payments_received")
    status = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment-{self.id} - {self.amount}"


# Models for Suppliers, Purchase Orders, Sales Orders, Invoices, Payment Methods, and Payments can be generated similarly.
