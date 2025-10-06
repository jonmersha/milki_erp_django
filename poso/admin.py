from django.contrib import admin
from .models import (
    Supplier, Customer,
    PurchaseOrder, PurchaseOrderItem,
    SalesOrder, SalesOrderItem,
    Payment, Invoice
)

# -----------------------------
# Inline Classes
# -----------------------------
class PurchaseOrderItemInline(admin.TabularInline):
    model = PurchaseOrderItem
    extra = 1
    readonly_fields = ('total_price',)


class SalesOrderItemInline(admin.TabularInline):
    model = SalesOrderItem
    extra = 1
    readonly_fields = ('total_price',)


# -----------------------------
# Supplier & Customer
# -----------------------------
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'phone', 'email', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('name', 'contact_person', 'phone', 'email')
    ordering = ('-created_at',)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('name', 'phone', 'email')
    ordering = ('-created_at',)


# -----------------------------
# Purchase Orders
# -----------------------------
@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'supplier', 'order_date', 'status')
    list_filter = ('status', 'order_date', 'supplier')
    search_fields = ('id', 'supplier__name')
    ordering = ('-order_date',)
    inlines = [PurchaseOrderItemInline]


@admin.register(PurchaseOrderItem)
class PurchaseOrderItemAdmin(admin.ModelAdmin):
    list_display = ('purchase_order', 'product', 'quantity', 'unit_price', 'status', 'total_price')
    list_filter = ('status', 'product')
    search_fields = ('product__name', 'purchase_order__id')
    readonly_fields = ('total_price',)


# -----------------------------
# Sales Orders
# -----------------------------
@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'order_date', 'status')
    list_filter = ('status', 'order_date', 'customer')
    search_fields = ('id', 'customer__name')
    ordering = ('-order_date',)
    inlines = [SalesOrderItemInline]


@admin.register(SalesOrderItem)
class SalesOrderItemAdmin(admin.ModelAdmin):
    list_display = ('sales_order', 'product', 'quantity', 'unit_price', 'total_price')
    search_fields = ('product__name', 'sales_order__id')
    readonly_fields = ('total_price',)


# -----------------------------
# Payments
# -----------------------------
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'sales_order', 'purchase_order', 'amount', 'method', 'status', 'created_at')
    list_filter = ('status', 'method')
    search_fields = ('id', 'sales_order__id', 'purchase_order__id')
    ordering = ('-created_at',)


# -----------------------------
# Invoices
# -----------------------------
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'sales_order', 'purchase_order', 'invoice_date', 'total_amount', 'status')
    list_filter = ('status', 'invoice_date')
    search_fields = ('id', 'sales_order__id', 'purchase_order__id')
    ordering = ('-invoice_date',)
