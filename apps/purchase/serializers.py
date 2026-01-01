from rest_framework import serializers
from .models import Supplier, PurchaseOrder, PurchaseOrderItem, GoodsReceivingNote

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = [
            'tracker',
            'name',
            'contact_person',
            'phone',
            'email', 
            'address', 
            'status']

class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    
    class Meta:
        model = PurchaseOrderItem
        fields = ['tracker', 'purchase_order', 'product', 'product_name', 'quantity', 'unit_price', 'status']
        read_only_fields = ['tracker']

class PurchaseOrderSerializer(serializers.ModelSerializer):
    # This allows the API to return the items list inside the Order object
    items = PurchaseOrderItemSerializer(many=True, read_only=True)
    supplier_name = serializers.ReadOnlyField(source='supplier.name')
    warehouse_name = serializers.ReadOnlyField(source='destination_store.name')

    class Meta:
        model = PurchaseOrder
        fields = ['tracker', 'supplier', 'supplier_name', 'destination_store', 'warehouse_name', 'order_date', 'status', 'items']
        read_only_fields = ['tracker', 'order_date']

# Specialized Serializer for the Add Item logic
class AddPurchaseItemSerializer(serializers.Serializer):
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all())
    warehouse = serializers.PrimaryKeyRelatedField(queryset=apps.get_model('inventory', 'Warehouse').objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=apps.get_model('inventory', 'Product').objects.all())
    quantity = serializers.IntegerField(min_value=1)
    unit_price = serializers.DecimalField(max_digits=12, decimal_places=2)