from datetime import timezone
from django.db import models
from apps.core.base import BaseModel
from apps.inventory.models import Stock, Warehouse
from apps.core.utility.uuidgen import cid, generate_custom_id
from django.db.models import F
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

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

class SalesOrder(models.Model):
    ORDER_OPTIONS = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    payment_status_options = [
        ('Unpaid', 'Unpaid'),
        ('Paid', 'Paid'),
        ('Refunded', 'Refunded'),
    ]
    id=models.CharField(max_length=20,primary_key=True,editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, null=True, blank=True,related_name='sales_orders')
    order_status=models.CharField(max_length=20,choices=ORDER_OPTIONS,default='Pending')
    order_date=models.DateTimeField(auto_now_add=True)
    payment_status=models.CharField(max_length=20,choices=payment_status_options,default='Unpaid')


    def save(self, *args, **kwargs):
       if not self.id:
           self.id = cid(prefix="SO", length=16)
       super().save(*args, **kwargs)
    def __str__(self):
        return f"Order {self.id} for {self.customer}"
    



# --------------------------------------------------------------------------
# Sales Item Model
class SalesItem(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('Unpaid', 'Unpaid'),
        ('Paid', 'Paid'),
        ('Refunded', 'Refunded'),
    ]
    id=models.CharField(max_length=20,primary_key=True,editable=False)
    sale_order=models.ForeignKey(
        SalesOrder,
        on_delete=models.CASCADE,
        null=False,blank=False,editable=True)
    product_name=models.ForeignKey(
        'inventory.Product',
        on_delete=models.PROTECT,
        null=False,blank=False,editable=True)
    source_whouse=models.ForeignKey(
        Warehouse,
        on_delete=models.PROTECT,
        null=False,blank=False,editable=True)
    inventory=models.ForeignKey(
        Stock,
        on_delete=models.PROTECT,
        null=False,blank=False,editable=True)
    
    quantity=models.PositiveIntegerField()
    price=models.DecimalField(max_digits=10, decimal_places=2)
    total_price=models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    status=models.CharField(default='Pending',max_length=20,choices=STATUS_CHOICES)
    payment_status=models.CharField(default='Unpaid',max_length=20,choices=PAYMENT_STATUS_CHOICES)
    reg_date=models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        self.total_price = self.price * self.quantity

        try:
            inventory_record = Stock.objects.get(product=self.product_name, warehouse=self.source_whouse)
        except ObjectDoesNotExist:
            return {"detail": "No inventory record found for the specified product and warehouse."}
        if inventory_record.quantity < self.quantity:
            return {"status": "insufficient_stock", "available_quantity": inventory_record.quantity}
        self.inventory = inventory_record
        if not self.id:
            self.id = cid(prefix="SI")
        if self.status == 'Pending':
            update_count = SalesItem.objects.filter(
                sale_order=self.sale_order,
                product_name=self.product_name,
                status='Pending'
            ).exclude(id=self.id).update(
                quantity=F('quantity') + self.quantity,
                price=self.price,
                total_price=F('price') * F('quantity'),
            )
            if update_count:
                return {"status": "merged", "update_count": update_count}
            super().save(*args, **kwargs)
            return self 
        elif self.status == 'Confirmed':
            confirmed = SalesItem.objects.filter(
                id=self.id,
                status='Pending'
            ).update(status='Confirmed')

            if confirmed:
                return {"status": "updated to confirmed", "id": self.id}
            return {"status": "no pending item found to confirm"}
        super().save(*args, **kwargs)
        return self
    def __str__(self):
        return f"Item {self.product_name} (x{self.quantity}) for Order {self.sale_order.id}"

# --------------------------------------------------------------------------------
class SalesTransaction(models.Model):
    id=models.CharField(max_length=20,primary_key=True,editable=False)
    sale_item=models.ForeignKey(
        SalesItem,
        on_delete=models.CASCADE,
        null=False,blank=False,editable=False)
    transaction_date=models.DateTimeField(auto_now_add=True)
    amount=models.DecimalField(max_digits=10, decimal_places=2)
    payment_method=models.CharField(max_length=50)
    bank_reference=models.CharField(max_length=100)
    payment_status=models.CharField(default='Unpaid')

    def save(self, *args, **kwargs):
       if not self.id:
           self.id = cid(prefix="ST")
       super().save(*args, **kwargs)

    def __str__(self):
        return f"Transaction {self.id} for Item {self.sale_item.id}"
