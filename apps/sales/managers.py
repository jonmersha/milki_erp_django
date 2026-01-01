# from django.db import models, transaction
# from django.core.exceptions import ValidationError

# class SalesItemManager(models.Manager):
#     def add_item_to_order(self, customer, product, warehouse, quantity, price):
#         # We wrap this in an atomic transaction to prevent race conditions
#         with transaction.atomic():
#             # 1. Get or Create a Pending Sales Order for this customer
#             from .models import SalesOrder, Stock
            
#             sales_order, created = SalesOrder.objects.get_or_create(
#                 customer=customer,
#                 order_status='Pending',
#                 defaults={'payment_status': 'Unpaid'}
#             )

#             # 2. Validate Stock availability
#             try:
#                 inventory_record = Stock.objects.select_for_update().get(
#                     product=product, 
#                     warehouse=warehouse
#                 )
#                 if inventory_record.quantity < quantity:
#                     raise ValidationError(f"Insufficient stock. {inventory_record.quantity} available.")
#             except Stock.DoesNotExist:
#                 raise ValidationError("No inventory record found for this product/warehouse.")

#             # 3. Check if this product already exists in the pending order
#             # We use select_for_update to lock the row for the increment
#             sales_item, item_created = self.get_queryset().select_for_update().get_or_create(
#                 sale_order=sales_order,
#                 product_name=product,
#                 source_whouse=warehouse,
#                 status='Pending',
#                 defaults={
#                     'quantity': quantity,
#                     'price': price,
#                     'inventory': inventory_record,
#                 }
#             )

#             if not item_created:
#                 # 4. Increment quantity if item already exists
#                 sales_item.quantity += quantity
#                 # Optionally update the price to the latest one provided
#                 sales_item.price = price 
#                 sales_item.save()
            
#             return sales_item