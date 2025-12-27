from django.contrib import admin
from .models import Customer, SalesOrder, SalesItem, SalesTransaction

class SalesItemInline(admin.TabularInline):
    model = SalesItem
    extra = 0
    readonly_fields = ('id', 'total_price')
    fields = ('product_name', 'source_whouse', 'quantity', 'price', 'total_price', 'status')

@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'order_status', 'payment_status', 'order_date')
    list_filter = ('order_status', 'payment_status')
    inlines = [SalesItemInline]
    readonly_fields = ('id', 'order_date')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'status')
    search_fields = ('name', 'email')


@admin.register(SalesTransaction)
class SalesTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'sale_item', 'amount', 'payment_method', 'transaction_date')