# from django.db import models, transaction

# from apps.purchase.models import GRNItem, GoodsReceivingNote

# class PurchaseOrderManager(models.Manager):
#     def add_item(self, product, quantity, unit_price, supplier_id=None, warehouse_id=None, po_id=None):
#         with transaction.atomic():
#             # 1. Get or Create the Purchase Order (Starts with "PO")
#             if po_id:
#                 purchase_order = self.get(id=po_id)
#             else:
#                 if not (supplier_id and warehouse_id):
#                     raise ValueError("Supplier and Warehouse are required for new orders.")
#                 purchase_order = self.create(
#                     supplier_id=supplier_id,
#                     destination_store_id=warehouse_id,
#                     status='pending'
#                 )

#             # 2. Add the Item (Starts with "POI")
#             from .models import PurchaseOrderItem
#             item = PurchaseOrderItem(
#                 purchase_order=purchase_order,
#                 product=product,
#                 quantity=quantity,
#                 unit_price=unit_price,
#                 status='pending'
#             )
#             # This triggers PurchaseOrderItem.save() logic
#             item.save()
            
#             return purchase_order
#     def create_grn_from_po(self, po_id, received_by, items_data):
#         # MOVE IMPORTS HERE to break the circularity
#         from .models import GoodsReceivingNote, GRNItem, PurchaseOrder
        
#         with transaction.atomic():
#             po = self.get(id=po_id)
            
#             grn = GoodsReceivingNote.objects.create(
#                 purchase_order=po,
#                 received_by=received_by
#             )
            
#             for item in items_data:
#                 GRNItem.objects.create(
#                     grn=grn,
#                     po_item_id=item['po_item_id'],
#                     quantity_received=item['qty']
#                 )
                
#             # Check if all items are received to close the PO
#             if not po.items.filter(status='pending').exists():
#                 po.status = 'received'
#                 po.save()
                
#             return grn
from django.db import models, transaction
from django.apps import apps  # Required for lazy loading

class PurchaseOrderManager(models.Manager):
    def add_item(self, product, quantity, unit_price, supplier_id=None, warehouse_id=None, po_id=None):
        # Access the PurchaseOrderItem model lazily
        PurchaseOrderItem = apps.get_model('purchase', 'PurchaseOrderItem')
        
        with transaction.atomic():
            if po_id:
                purchase_order = self.get(id=po_id)
            else:
                purchase_order = self.create(
                    supplier_id=supplier_id,
                    destination_store_id=warehouse_id,
                    status='pending'
                )

            item = PurchaseOrderItem(
                purchase_order=purchase_order,
                product=product,
                quantity=quantity,
                unit_price=unit_price,
                status='pending'
            )
            item.save()
            return purchase_order

    def create_grn_from_po(self, po_id, received_by, items_data):
        # Access models lazily using apps.get_model('app_label', 'ModelName')
        GoodsReceivingNote = apps.get_model('purchase', 'GoodsReceivingNote')
        GRNItem = apps.get_model('purchase', 'GRNItem')
        
        with transaction.atomic():
            # 'self.model' refers to PurchaseOrder because the manager is attached to it
            po = self.select_for_update().get(id=po_id)
            
            grn = GoodsReceivingNote.objects.create(
                purchase_order=po,
                received_by=received_by
            )
            
            for item in items_data:
                GRNItem.objects.create(
                    grn=grn,
                    po_item_id=item['po_item_id'],
                    quantity_received=item['qty']
                )
                
            # Use related_name 'items' to check pending status
            if not po.items.filter(status='pending').exists():
                po.status = 'received'
                po.save(update_fields=['status'])
                
            return grn