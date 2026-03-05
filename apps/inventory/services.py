# apps/inventory/services.py
from django.db import transaction
from django.db.models import F
from .models import Stock, InventoryMovementLog

class InventoryService:
    @staticmethod
    def update_stock_from_grn(grn):
        """
        Increases stock levels based on a confirmed GRN.
        """
        with transaction.atomic():
            po = grn.purchase_order
            warehouse = po.destination_store
            
            # We iterate through the items in the PO
            # Note: For more precision, you might want a GRNItem model
            # But here we assume receipt of all PO items for simplicity
            for item in po.items.filter(status='Pending'):
                # 1. Update or Create Stock record
                stock, created = Stock.objects.select_for_update().get_or_create(
                    warehouse=warehouse,
                    product=item.product,
                    defaults={'quantity': 0, 'unit_price': item.unit_price}
                )
                
                # 2. Update Quantity and Unit Price (Weighted Average or Latest)
                stock.quantity += item.quantity
                stock.unit_price = item.unit_price # Or implement Moving Average Price logic
                stock.save()
                
                # 3. Create Movement Log
                InventoryMovementLog.objects.create(
                    product=item.product,
                    quantity=item.quantity,
                    movement_type='inbound',
                    reason='purchase',
                    destination_warehouse=warehouse,
                )
                
                # 4. Mark PO Item as Received
                item.status = 'Received'
                item.save()

            # 5. Update PO Status
            po.status = 'Completed'
            po.save()