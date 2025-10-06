# inventory/admin.py

from django.contrib import admin
from .models import Warehouse, Product, Stock, InventoryMovement,ProductPackage

# @admin.register(ProductPackage)
# class ProductPackageAdmin(admin.ModelAdmin):
#     list_display = ('name')
#     search_fields = ('name',)
@admin.register(ProductPackage)
class ProductPackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_authorized', 'created_at')
    search_fields = ('name',)
    list_filter = ('is_authorized',)
    readonly_fields = ('created_at', 'updated_at')


# -----------------------------
# Warehouse Admin
# -----------------------------
@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'capacity', 'status', 'is_authorized', 'created_at')
    search_fields = ('name', 'location')
    list_filter = ('status', 'is_authorized')
    # readonly_fields = ('created_at', 'updated_at')


# -----------------------------
# Product Admin
# -----------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit_price', 'status', 'is_authorized', 'created_at')
    search_fields = ('name',)
    list_filter = ('status', 'is_authorized')
    readonly_fields = ('created_at', 'updated_at')


# -----------------------------
# Stock Admin
# -----------------------------

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'product',
        'warehouse',
        'quantity',
        'unit_price',
        'total_value',
        'minimum_threshold',
        'last_updated',
        'created_at',
    )
    search_fields = ('product__name', 'warehouse__name')
    list_filter = ('warehouse', 'product')
    readonly_fields = ('last_updated', 'created_at', 'updated_at')

    def get_queryset(self, request):
        """
        Optionally override queryset to prefetch related models
        for performance.
        """
        qs = super().get_queryset(request)
        return qs.select_related('product', 'warehouse')

# -----------------------------
# InventoryMovement Admin
# -----------------------------
@admin.register(InventoryMovement)
class InventoryMovementAdmin(admin.ModelAdmin):
    list_display = (
        'product', 'movement_type', 'quantity',
        'source_warehouse', 'destination_warehouse',
        'date', 'status', 'is_authorized'
    )
    search_fields = ('product__name', 'source_warehouse__name', 'destination_warehouse__name')
    list_filter = ('movement_type', 'status', 'is_authorized')
    readonly_fields = ('date', 'created_at', 'updated_at')
