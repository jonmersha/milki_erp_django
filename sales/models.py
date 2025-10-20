from django.db import models
from core.base import BaseModel
from inventory.models import Stock, Warehouse
from poso.models import Customer
from core.utility.uuidgen import cid
from django.db.models import F
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction


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
        inventory_record = Stock.objects.get(product=self.product_name, warehouse=self.source_whouse)

        if inventory_record:
            if inventory_record.quantity < self.quantity:
                return {"status": "insufficient_stock", "available_quantity": inventory_record.quantity}
            self.inventory = inventory_record
        else:
            raise {"detail": "No inventory record found for the specified product and warehouse."}

        if not self.id:
            self.id = cid(prefix="SI")

        with transaction.atomic():
            if self.status == 'Pending':
                # Lock the row to prevent race conditions
                existing_item = SalesItem.objects.select_for_update().filter(
                    sale_order=self.sale_order,
                    product_name=self.product_name,
                    status='Pending'
                ).first()

                if existing_item:
                    # Merge safely inside transaction
                    existing_item.quantity += self.quantity
                    existing_item.price += self.price
                    existing_item.total_price = existing_item.quantity * existing_item.price
                    existing_item.save(update_fields=['quantity', 'price', 'total_price'])
                    return existing_item  # return merged object
                else:
                    # No existing pending item, save new
                    super().save(*args, **kwargs)
                    return self

            elif self.status == 'Confirmed':
                # Confirm only if pending exists
                pending_item = SalesItem.objects.select_for_update().filter(
                    id=self.id,
                    status='Pending'
                ).first()
                if pending_item:
                    pending_item.status = 'Confirmed'
                    pending_item.save(update_fields=['status'])
                    return pending_item
                return {"status": "no pending item found to confirm"}

            else:
                # Default save for other statuses
                super().save(*args, **kwargs)
                return self

    # def save(self, *args, **kwargs):
    #     self.total_price = self.price * self.quantity
    #     inventory_record = Stock.objects.get(product=self.product_name, warehouse=self.source_whouse)
        
    #     if inventory_record:
    #         #check for sufficient stock
    #         if inventory_record.quantity < self.quantity:
    #             return {"status": "insufficient_stock", "available_quantity": inventory_record.quantity}
    #         self.inventory = inventory_record
    #     else:
    #         raise {"detail": "No inventory record found for the specified product and warehouse."}

    #     if not self.id:
    #         self.id = cid(prefix="SI")
    #     with transaction.atomic():

    #         if self.status == 'Pending':

    #             existing_item = SalesItem.objects.select_for_update().filter(
    #                     sale_order=self.sale_order,
    #                     product_name=self.product_name,
    #                     status='Pending'
    #                 ).first()
    #             if existing_item:
    #                 # If an existing item is found, merge the quantities
    #                 existing_item.quantity += self.quantity
    #                 existing_item.price += self.price
    #                 existing_item.total_price = existing_item.quantity * existing_item.price
    #                 # existing_item.save(update_fields=['quantity', 'price', 'total_price'])
    #                 return existing_item 
    #             else:
    #                 super().save(*args, **kwargs)
    #                 return self
    #         # Try merging with an existing pending record for the same product & order
    #         # update_count=SalesItem.objects.filter(
    #         #     sale_order=self.sale_order,
    #         #     product_name=self.product_name,
    #         #     status='Pending'
    #         # ).update(
    #         #     quantity=F('quantity') + self.quantity,
    #         #     price=F('price') + self.price , # preserve accumulated total
    #         #     total_price=F('price') * F('quantity'),

    #         # )
    #         # super().save(*args, **kwargs)
    #         # # if merge succeeded, skip saving a duplicate


    #         # merged_item = SalesItem.objects.filter(
    #         #                 sale_order=self.sale_order,
    #         #                 product_name=self.product_name,
    #         #                 status='Pending'
    #         # #             )
    #         # if update_count:
    #         #     merged_item = SalesItem.objects.filter(
    #         #         sale_order=self.sale_order,
    #         #         product_name=self.product_name,
    #         #         status='Pending'
    #         #     ).select_related(
    #         #         'sale_order', 'product_name', 'source_whouse', 'inventory'
    #         #     ).first()  # use first() to avoid DoesNotExist
    #         #     return merged_item
            
    #         # else:
    #         #     # no existing pending item, proceed to save new
    #         #     super().save(*args, **kwargs)
    #         #     return {"status": "new item saved", "id": self.id}

    #         elif self.status == 'Confirmed':
    #             # move the item from pending to confirmed
    #             confirmed = SalesItem.objects.filter(
    #                 id=self.id,
    #                 status='Pending'
    #             ).update(status='Confirmed')
    #             if confirmed:
    #                 return {"status": "updated to confirmed", "id": self.id}
    #             return {"status": "no pending item found to confirm"}

       
# def save(self, *args, **kwargs):
#     self.total_price = self.price * self.quantity

#     try:
#         inventory_record = Stock.objects.get(product=self.product_name, warehouse=self.source_whouse)
#     except ObjectDoesNotExist:
#         return {"detail": "No inventory record found for the specified product and warehouse."}

#     # check for sufficient stock
#     if inventory_record.quantity < self.quantity:
#         return {"status": "insufficient_stock", "available_quantity": inventory_record.quantity}

#     # assign inventory
#     self.inventory = inventory_record.id

#     # auto-generate id
#     if not self.id:
#         self.id = cid(prefix="SI")

#     # handle pending state merging
#     if self.status == 'Pending':
#         update_count = SalesItem.objects.filter(
#             sale_order=self.sale_order,
#             product_name=self.product_name,
#             status='Pending'
#         ).exclude(id=self.id).update(
#             quantity=F('quantity') + self.quantity,
#             price=F('price') + self.price,
#             total_price=F('price') * F('quantity'),
#         )

#         # if merged → return info message
#         if update_count:
#             return {"status": "merged", "update_count": update_count}

#         # if new pending item → save normally
#         super().save(*args, **kwargs)
#         return self  # ✅ return full object

#     elif self.status == 'Confirmed':
#         confirmed = SalesItem.objects.filter(
#             id=self.id,
#             status='Pending'
#         ).update(status='Confirmed')

#         if confirmed:
#             return {"status": "updated to confirmed", "id": self.id}
#         return {"status": "no pending item found to confirm"}

#     # default: just save normally
#     super().save(*args, **kwargs)
#     return self
def __str__(self):
    return f"Item {self.product_name} (x{self.quantity}) for Order {self.sale_order.id}"









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