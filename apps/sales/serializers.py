from rest_framework import serializers
from django.apps import apps
from django.db import transaction
from .models import Customer, SalesOrder, SalesItem, SalesTransaction

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'tracker', 'name', 'phone', 'email', 'address', 'status']
        read_only_fields = ['id', 'tracker']

class SalesItemSerializer(serializers.ModelSerializer):
    # Fetching related names for UI display
    product_name_display = serializers.ReadOnlyField(source='product_name.name')
    warehouse_name = serializers.ReadOnlyField(source='source_whouse.name')
    
    class Meta:
        model = SalesItem
        fields = [
            'id', 'tracker', 'sale_order', 'product_name', 
            'product_name_display', 'source_whouse', 'warehouse_name',
            'quantity', 'price', 'total_price', 'status'
        ]
        read_only_fields = ['id', 'tracker', 'total_price', 'sale_order']

class SalesOrderSerializer(serializers.ModelSerializer):
    # Nested items for the Detail view
    items = SalesItemSerializer(many=True, read_only=True)
    customer_name = serializers.ReadOnlyField(source='customer.name')
    
    # Summary calculation
    item_count = serializers.SerializerMethodField()

    class Meta:
        model = SalesOrder
        fields = [
            'id', 'tracker', 'customer', 'customer_name', 
            'order_status', 'payment_status', 'order_date', 
            'item_count', 'items'
        ]
        read_only_fields = ['id', 'tracker', 'order_date']

    def get_item_count(self, obj):
        return obj.items.count()

# --- SPECIALIZED ACTION SERIALIZER FOR SALES ---

class AddSalesItemSerializer(serializers.Serializer):
    """
    Specifically used to trigger SalesOrder.objects.add_item_to_order
    from the frontend (Flutter).
    """
    customer = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all()
    )
    warehouse = serializers.PrimaryKeyRelatedField(
        queryset=apps.get_model('inventory', 'Warehouse').objects.all()
    )
    product = serializers.PrimaryKeyRelatedField(
        queryset=apps.get_model('inventory', 'Product').objects.all()
    )
    quantity = serializers.IntegerField(min_value=1)
    price = serializers.DecimalField(max_digits=12, decimal_places=2)
    force_new_order = serializers.BooleanField(default=False, required=False)

    def validate(self, data):
        # Ensure customer is active before allowing a sale
        if data['customer'].status != 'active':
            raise serializers.ValidationError("Cannot create sales for inactive customers.")
        return data

# # --- TRANSACTION SERIALIZER (Replaces GRN logic) ---

# class SalesTransactionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SalesTransaction
#         fields = [
#             'id', 'tracker', 'sale_item', 'transaction_date', 
#             'amount', 'payment_method', 'bank_reference', 'payment_status'
#         ]
#         read_only_fields = ['id', 'tracker', 'transaction_date']
class SalesTransactionSerializer(serializers.ModelSerializer):
    # Helpful display fields for the mobile UI
    product_name = serializers.ReadOnlyField(source='sale_item.product_name.name')
    item_tracker = serializers.ReadOnlyField(source='sale_item.tracker')

    class Meta:
        model = SalesTransaction
        fields = [
            'id', 'tracker', 'sale_item', 'product_name', 'item_tracker',
            'transaction_date', 'amount', 'payment_method', 
            'bank_reference', 'payment_status'
        ]
        read_only_fields = ['id', 'tracker', 'transaction_date']