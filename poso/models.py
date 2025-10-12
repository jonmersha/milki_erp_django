# pos/models.py

import uuid
from django.db import models

from core.base import BaseModel
from inventory.models import Product
from django.utils import timezone
from core.utility.uuidgen import generate_custom_id

# -----------------------------
# Partners: Supplier & Customer
# -----------------------------
class Supplier(BaseModel):
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
    contact_person = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True, null=True)
    def save(self, *args, **kwargs):
        if not self.id:
            partition = timezone.now().strftime("%Y%m%d")
            self.id = generate_custom_id(prefix="SUP", partition=partition, length=16)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name


class Customer(BaseModel):
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
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True, null=True)
    def save(self, *args, **kwargs):
        if not self.id:
            partition = timezone.now().strftime("%Y%m%d")
            self.id = generate_custom_id(prefix="CUS", partition=partition, length=16)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name

# -----------------------------
# Purchase Orders (PO + POI)
# -----------------------------
class PurchaseOrder(BaseModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('inactive', 'Inactive'),
        ('received','Received')
    ]
    id = models.CharField(
        max_length=16,
        primary_key=True,
        editable=False,
        unique=True
    )
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    def save(self, *args, **kwargs):
        if not self.id:
            partition = timezone.now().strftime("%Y%m%d")
            self.id = generate_custom_id(prefix="PO", partition=partition, length=16)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"PO-{self.id}"
    


class PurchaseOrderItem(BaseModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('inactive', 'Inactive'),
        ('received','Received')
        ]
    id = models.CharField(
        max_length=16,
        primary_key=True,
        editable=False,
        unique=True
    )
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    def save(self, *args, **kwargs):
        if not self.id:
            partition = timezone.now().strftime("%Y%m%d")
            self.id = generate_custom_id(prefix="POI", partition=partition, length=16)
        super().save(*args, **kwargs)

    @property
    def total_price(self):
        return self.quantity * self.unit_price
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['purchase_order', 'product'], name='unique_product_per_PO')
        ]


# -----------------------------
# Sales Orders (SO + SOI)
# -----------------------------
class SalesOrder(BaseModel):
    STATUS_CHOICES = [
        ('draft','Draft'),
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('received','Received')
        ]
    id = models.CharField(
        max_length=16,
        primary_key=True,
        editable=False,
        unique=True
    )
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,default='draft')
    def save(self, *args, **kwargs):
        if not self.id:
            partition = timezone.now().strftime("%Y%m%d")
            self.id = generate_custom_id(prefix="SO", partition=partition, length=16)
        super().save(*args, **kwargs)


    def __str__(self):
        return f"SO-{self.id}"


class SalesOrderItem(BaseModel):
    id = models.CharField(
        max_length=16,
        primary_key=True,
        editable=False,
        unique=True
    )
    sales_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.id:
            partition = timezone.now().strftime("%Y%m%d")
            self.id = generate_custom_id(prefix="SOI", partition=partition, length=16)
        super().save(*args, **kwargs)


    @property
    def total_price(self):
        return self.quantity * self.unit_price
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['sales_order', 'product'], name='unique_product_per_SO')
        ]


# -----------------------------
# Payments
# -----------------------------
class Payment(BaseModel):
    id = models.CharField(
        max_length=16,
        primary_key=True,
        editable=False,
        unique=True
    )
    sales_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, null=True, blank=True)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    method = models.CharField(max_length=50, choices=[('cash','Cash'), ('card','Card'), ('online','Online')])
    status = models.CharField(max_length=20, choices=[('pending','Pending'), ('paid','Paid')])
    def save(self, *args, **kwargs):
        if not self.id:
            partition = timezone.now().strftime("%Y%m%d")
            self.id = generate_custom_id(prefix="PYT", partition=partition, length=16)
        super().save(*args, **kwargs)


    def __str__(self):
        if self.sales_order:
            return f"Payment-SO-{self.sales_order.id}"
        if self.purchase_order:
            return f"Payment-PO-{self.purchase_order.id}"


# -----------------------------
# Invoices
# -----------------------------
class Invoice(BaseModel):
    id = models.CharField(
        max_length=16,
        primary_key=True,
        editable=False,
        unique=True
    )
    sales_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, null=True, blank=True)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, null=True, blank=True)
    invoice_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=14, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('draft','Draft'), ('sent','Sent'), ('paid','Paid')])
    def save(self, *args, **kwargs):
        if not self.id:
            partition = timezone.now().strftime("%Y%m%d")
            self.id = generate_custom_id(prefix="INV", partition=partition, length=16)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice-{self.id}"
