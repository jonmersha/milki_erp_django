# from django.contrib import admin
# from .models import Supplier, PurchaseOrder, PurchaseOrderItem

# # --- Inlines ---

# # class PurchaseOrderItemInline(admin.TabularInline):
# #     """Allows adding/editing items directly inside the Purchase Order page."""
# #     model = PurchaseOrderItem
# #     extra = 1
# #     fields = ('product', 'quantity', 'unit_price', 'status', 'tracker')
# #     readonly_fields = ('tracker',)
# #     autocomplete_fields = ('product',)  # Improved UX for large inventory

# # --- Model Admins ---

# @admin.register(Supplier)
# class SupplierAdmin(admin.ModelAdmin):
#     list_display = ('id', 'tracker', 'name', 'contact_person', 'phone', 'status')
#     list_filter = ('status',)
#     search_fields = ('name', 'tracker', 'contact_person')
#     ordering = ('name',)

# @admin.register(PurchaseOrder)
# class PurchaseOrderAdmin(admin.ModelAdmin):
#     list_display = ('id', 'tracker', 'supplier', 'destination_store', 'order_date', 'status')
#     list_filter = ('status', 'destination_store', 'order_date')
#     search_fields = ('tracker', 'supplier__name', 'destination_store__name')
#     inlines = [PurchaseOrderItemInline]
#     ordering = ('-order_date',)
#     actions = ['mark_as_received']

#     @admin.action(description="Mark selected orders as Received")
#     def mark_as_received(self, request, queryset):
#         """Custom action to update PO status and trigger downstream logic."""
#         for po in queryset:
#             po.status = 'received'
#             po.save()
#             # This triggers status updates for items if logic is in PO save
#             # Or you can explicitly update items here:
#             po.items.update(status='received')
#             for item in po.items.all():
#                  item.save() # Triggers the _update_stock_and_log() in PurchaseOrderItem

# @admin.register(PurchaseOrderItem)
# class PurchaseOrderItemAdmin(admin.ModelAdmin):
#     list_display = ('id', 'tracker', 'purchase_order', 'product', 'quantity', 'unit_price', 'status')
#     list_filter = ('status',)
#     search_fields = ('tracker', 'product__name', 'purchase_order__tracker')
#     readonly_fields = ('tracker',)