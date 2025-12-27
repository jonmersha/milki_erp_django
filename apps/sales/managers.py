from django.db import models, transaction
from django.apps import apps
from django.db.models import F

class SalesOrderManager(models.Manager):
    def add_item(self, sale_order_id, product, warehouse, quantity, price):
        # Lazy load models to avoid circular imports
        SalesItem = apps.get_model('sales', 'SalesItem')
        Stock = apps.get_model('inventory', 'Stock')

        with transaction.atomic():
            # 1. Lock and check stock
            try:
                inventory = Stock.objects.select_for_update().get(
                    product=product, warehouse=warehouse
                )
            except Stock.DoesNotExist:
                raise ValueError("No inventory record found for this product/warehouse.")

            if inventory.quantity < quantity:
                raise ValueError(f"Insufficient stock. Available: {inventory.quantity}")

            # 2. Handle Merging for 'Pending' items
            # If same product/warehouse/order exists in Pending, update it
            item, created = SalesItem.objects.get_or_create(
                sale_order_id=sale_order_id,
                product_name=product,
                source_whouse=warehouse,
                status='Pending',
                defaults={
                    'quantity': quantity,
                    'price': price,
                    'inventory': inventory
                }
            )

            if not created:
                item.quantity = F('quantity') + quantity
                item.price = price  # Update to latest price
                item.save()
                item.refresh_from_db()
            
            return item