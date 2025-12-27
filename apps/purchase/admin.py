from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import GRNItem, GoodsReceivingNote, Supplier, PurchaseOrder, PurchaseOrderItem

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'contact_person', 'phone', 'status')
    list_filter = ('status',)
    search_fields = ('name', 'contact_person', 'email', 'id')
    ordering = ('name',)
    readonly_fields = ('id',)

class PurchaseOrderItemInline(admin.TabularInline):
    model = PurchaseOrderItem
    extra = 1
    fields = ('product', 'quantity', 'unit_price', 'status')
    # We make product read-only if the item is already received to prevent errors
    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status == 'received':
            return ('product', 'quantity', 'unit_price', 'status')
        return ()

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'supplier', 'destination_store', 'order_date', 'status')
    list_filter = ('status', 'order_date', 'destination_store')
    search_fields = ('id', 'supplier__name', 'destination_store__name')
    readonly_fields = ('id', 'order_date')
    inlines = [PurchaseOrderItemInline]
    
    # Optional: Logic to prevent editing the PO if it's already received
    def save_formset(self, request, form, formset, change):
        # This ensures the model's atomic save logic is triggered
        instances = formset.save(commit=False)
        for instance in instances:
            instance.save()
        formset.save_m2m()

@admin.register(PurchaseOrderItem)
class PurchaseOrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'purchase_order', 'product', 'quantity', 'unit_price', 'status')
    list_filter = ('status', 'purchase_order__order_date')
    search_fields = ('id', 'purchase_order__id', 'product__name')
    readonly_fields = ('id',)
# 3. Items inside the GRN
class GRNItemInline(admin.TabularInline):
    model = GRNItem
    extra = 0
    fields = ('po_item', 'quantity_received')
@admin.register(GoodsReceivingNote)
class GoodsReceivingNoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'purchase_order', 'received_by', 'received_date', 'delivery_note_number')
    list_filter = ('received_date',)
    search_fields = ('id', 'purchase_order__id', 'received_by')
    readonly_fields = ('id', 'received_date')
    inlines = [GRNItemInline]

@admin.register(GRNItem)
class GRNItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'grn', 'get_product', 'quantity_received')
    readonly_fields = ('id',)

    def get_product(self, obj):
        return obj.po_item.product
    get_product.short_description = 'Product'