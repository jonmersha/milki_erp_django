
from inventory.serializers import ProductSerializer
from poso.serializers import CustomerSerializer
from .models import SalesItem, SalesOrder
from rest_framework import serializers


class SalesOrderSerializer(serializers.ModelSerializer):
    customer=CustomerSerializer(read_only=True)
    class Meta:
        model = SalesOrder
        fields = ['id', 'customer', 'order_date', 'order_status', 'payment_status']

class SalesItemSerializer(serializers.ModelSerializer):
    # product_name=ProductSerializer(read_only=True)
    # sale_order=SalesOrderSerializer(read_only=True)
    # make it is intenally coalculated field in the model

    # total_price=serializers.DecimalField(max_digits=10, decimal_places=2,read_only=True)
    # inventory=serializers.CharField(source='inventory.id', read_only=True)

    class Meta:
        model = SalesItem
        fields = ['id', 'sale_order', 'product_name','source_whouse', 'inventory','quantity', 'price', 'total_price', 'status', 'payment_status']
        read_only_fields = ['total_price', 'inventory']