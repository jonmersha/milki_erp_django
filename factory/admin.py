from .models import *
from django.contrib import admin, messages
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.utils.html import format_html, urlencode
from django.urls import reverse

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name',  'membership',]
    list_editable = ['membership']
    list_per_page = 10
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
# 2. Company
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'customer', 'company_status', 'created_at', 'updated_at']
    search_fields = ['name']
    list_filter = ['company_status', 'created_at']


# 3. Factory
@admin.register(Factory)
class FactoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'company', 'is_operational', 'is_authorized', 'created_at', 'updated_at']
    search_fields = ['name', 'city', 'admin_region']
    list_filter = ['is_operational', 'is_authorized', 'company']


# 4. Warehouse
@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['id', 'factory', 'capacity', 'status', 'is_authorized', 'created_at', 'updated_at']
    list_filter = ['status', 'is_authorized', 'factory']


# 5. Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


# 6. Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name', 'category', 'company', 'status', 'is_authorized', 'created_at', 'updated_at']
    search_fields = ['code', 'name']
    list_filter = ['status', 'is_authorized', 'company', 'category']


# 7. Stock
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'warehouse', 'quantity', 'unit_price', 'last_updated', 'is_authorized']
    list_filter = ['is_authorized', 'warehouse', 'product']


# 8. Stock Movement Log
@admin.register(StockMovementLog)
class StockMovementLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'movement_type', 'quantity', 'source_factory', 'destination_factory', 'logged_at', 'is_authorized']
    list_filter = ['movement_type', 'is_authorized', 'source_factory', 'destination_factory']


# 9. Supplier
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['id', 'supplier_name', 'company', 'supplier_status', 'is_authorized', 'created_at', 'updated_at']
    search_fields = ['supplier_name', 'supplier_contact_person']
    list_filter = ['supplier_status', 'is_authorized', 'company']


# 10. Purchase Order
@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'supplier', 'order_status', 'payment_status', 'placed_at', 'is_authorized']
    list_filter = ['order_status', 'payment_status', 'is_authorized']
    search_fields = ['supplier__supplier_name']


# 11. Purchase Order Item
@admin.register(PurchaseOrderItem)
class PurchaseOrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'purchase_order', 'product', 'quantity', 'unit_price', 'warehouse', 'factory']
    search_fields = ['product__name']
    list_filter = ['warehouse', 'factory']


# 12. Sales Order
@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'to_customer', 'order_status', 'payment_status', 'placed_at', 'is_authorized']
    list_filter = ['order_status', 'payment_status', 'is_authorized']
    search_fields = ['to_customer__first_name', 'to_customer__last_name']


# 13. Sales Order Item
@admin.register(SalesOrderItem)
class SalesOrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'sales_order', 'product', 'quantity', 'unit_price', 'total_price', 'factory', 'warehouse']
    search_fields = ['product__name']
    list_filter = ['factory', 'warehouse']


# 14. Invoice
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'invoice_number', 'invoice_type', 'sales_order', 'purchase_order', 'customer', 'supplier', 'issue_date', 'status']
    list_filter = ['invoice_type', 'status']
    search_fields = ['invoice_number']


# 15. Invoice Item
@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'invoice', 'product', 'quantity', 'unit_price', 'total_price']
    search_fields = ['product__name']
    list_filter = ['invoice']


# 16. Payment Method
@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['id', 'method_name', 'description']
    search_fields = ['method_name']


# 17. Payment
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'invoice', 'amount', 'method', 'payer', 'supplier', 'payment_date', 'status']
    list_filter = ['method', 'status', 'payment_date']
    search_fields = ['invoice__invoice_number', 'payer__first_name', 'supplier__supplier_name']
