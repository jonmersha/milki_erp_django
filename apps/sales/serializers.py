from rest_framework import serializers
from django.apps import apps
from .models import Customer, SalesOrder, SalesItem, SalesTransaction

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'tracker', 'name', 'phone', 'email', 'address', 'status']
        read_only_fields = ['id', 'tracker']

class SalesTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesTransaction
        fields = ['id', 'tracker', 'sale_item', 'transaction_date', 'amount', 'payment_method', 'bank_reference', 'payment_status']
        read_only_fields = ['id', 'tracker', 'transaction_date']

class SalesItemSerializer(serializers.ModelSerializer):
    product_name_display = serializers.CharField(source='product_name.name', read_only=True)
    warehouse_name = serializers.CharField(source='source_whouse.name', read_only=True)

    class Meta:
        model = SalesItem
        fields = [
            'id', 'tracker', 'sale_order', 'product_name', 'product_name_display',
            'source_whouse', 'warehouse_name', 'quantity', 'price', 'total_price', 'status'
        ]
        read_only_fields = ['id', 'tracker', 'total_price', 'sale_order']

class SalesOrderSerializer(serializers.ModelSerializer):
    items = SalesItemSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)

    class Meta:
        model = SalesOrder
        fields = ['id', 'tracker', 'customer', 'customer_name', 'order_status', 'payment_status', 'order_date', 'items']
        read_only_fields = ['id', 'tracker', 'order_date']

# Special Serializer for the "Add Item" Action
class AddSalesItemSerializer(serializers.Serializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=apps.get_model('inventory', 'Product').objects.all())
    warehouse = serializers.PrimaryKeyRelatedField(queryset=apps.get_model('inventory', 'Warehouse').objects.all())
    quantity = serializers.IntegerField(min_value=1)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)