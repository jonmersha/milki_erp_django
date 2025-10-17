# inventory/admin.py

from django.contrib import admin
from .models import Warehouse, Product, Stock, InventoryMovementLog,ProductPackage,StockTransfer

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
# @admin.register(InventoryMovementLog)
# class InventoryMovementLogAdmin(admin.ModelAdmin):
#     list_display = (
#         'id',
#         'product',
#         'date',
#         'movement_type',
#         'reason',
#         'get_warehouse',
#         'quantity',
#         'unit_price',
#         'status'
#     )

#     list_filter = (
#         'movement_type',
#         'reason',
#         'status',
#         'date',
#         'warehouse'
#     )

#     search_fields = (
#         'id',
#         'product__name',
#         'remarks'
#     )

#     ordering = ('-date',)

#     def get_warehouse(self, obj):
#         return obj.warehouse.name if obj.warehouse else None
#     get_warehouse.short_description = 'Warehouse'

# -----------------------------
# StockTransfer Admin
# -----------------------------
@admin.register(StockTransfer)
class StockTransferAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "source_warehouse",
        "destination_warehouse",
        "quantity",
        "status",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "source_warehouse", "destination_warehouse", "product")
    search_fields = ("id", "product__name", "source_warehouse__name", "destination_warehouse__name")
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("-created_at",)
    fieldsets = (
        ("Transfer Details", {
            "fields": (
                "id",
                "product",
                "source_warehouse",
                "destination_warehouse",
                "quantity",
                "status",
                "remarks",
            )
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        """
        Prevent editing certain fields after creation.
        """
        if obj:  # when editing existing transfer
            return self.readonly_fields + ("product", "source_warehouse", "destination_warehouse")
        return self.readonly_fields
