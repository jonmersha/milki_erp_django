from django.apps import apps
from rest_framework import serializers

from .models import Customer, SalesOrder, SalesItem, SalesTransaction

from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'id', 
            'name', 
            'phone', 
            'email', 
            'address', 
            'status',
            'created_at', # Inherited from BaseModel
            'updated_at'  # Inherited from BaseModel
        ]
        # ID and timestamps should never be sent by the client
        read_only_fields = ('id', 'created_at', 'updated_at')

class SalesItemSerializer(serializers.ModelSerializer):
    product_name_display = serializers.ReadOnlyField(source='product_name.name')
    warehouse_name = serializers.ReadOnlyField(source='source_whouse.name')

    class Meta:
        model = SalesItem
        fields = [
            'id', 'sale_order', 'product_name', 'product_name_display',
            'source_whouse', 'warehouse_name', 'quantity', 'price', 
            'total_price', 'status', 'payment_status'
        ]
        read_only_fields = ('id', 'total_price')

class SalesOrderSerializer(serializers.ModelSerializer):
    items = SalesItemSerializer(many=True, read_only=True)
    customer_name = serializers.ReadOnlyField(source='customer.name')
    
    class Meta:
        model = SalesOrder
        fields = [
            'id', 'customer', 'customer_name', 'order_status', 
            'payment_status', 'order_date', 'items'
        ]
        read_only_fields = ('id', 'order_date')

class AddSalesItemSerializer(serializers.Serializer):
    customer = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), 
        required=False, 
        allow_null=True
    )
    sale_order = serializers.PrimaryKeyRelatedField(
        queryset=SalesOrder.objects.all(), 
        required=False, 
        allow_null=True
    )
    # Use a lambda or a property to delay the queryset evaluation
    product = serializers.PrimaryKeyRelatedField(
        queryset=apps.get_model('inventory', 'Product').objects.all()
    )
    warehouse = serializers.PrimaryKeyRelatedField(
        queryset=apps.get_model('inventory', 'Warehouse').objects.all()
    )
    quantity = serializers.IntegerField(min_value=1)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    # REFINED APPROACH: Override __init__ to set querysets at runtime
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Product = apps.get_model('inventory', 'Product')
        Warehouse = apps.get_model('inventory', 'Warehouse')
        self.fields['product'].queryset = Product.objects.all()
        self.fields['warehouse'].queryset = Warehouse.objects.all()
class SalesTransactionSerializer(serializers.ModelSerializer):
    # Helpful read-only fields for the Frontend
    product_name = serializers.ReadOnlyField(source='sale_item.product_name.name')
    order_id = serializers.ReadOnlyField(source='sale_item.sale_order.id')
    
    class Meta:
        model = SalesTransaction
        fields = [
            'id', 
            'sale_item', 
            'order_id',
            'product_name',
            'amount', 
            'payment_method', 
            'bank_reference', 
            'payment_status',
            'transaction_date'
        ]
        read_only_fields = ('id', 'transaction_date')

    def validate_amount(self, value):
        """Ensure payment doesn't exceed the item price (optional but recommended)"""
        if value <= 0:
            raise serializers.ValidationError("Transaction amount must be greater than zero.")
        return value