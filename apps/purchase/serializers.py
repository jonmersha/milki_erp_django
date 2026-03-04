# from rest_framework import serializers
# from .models import Supplier, PurchaseOrder, PurchaseOrderItem, GoodsReceivingNote
# from django.apps import apps
# class SupplierSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Supplier
#         fields = [
#             'id',
#             'tracker',
#             'name',
#             'contact_person',
#             'phone',
#             'email', 
#             'address', 
#             'status']

# class PurchaseOrderItemSerializer(serializers.ModelSerializer):
#     product_name = serializers.ReadOnlyField(source='product.name')
    
#     class Meta:
#         model = PurchaseOrderItem
#         fields = ['id','tracker', 'purchase_order', 'product', 'product_name', 'quantity', 'unit_price', 'status']
#         read_only_fields = ['tracker']

# class PurchaseOrderSerializer(serializers.ModelSerializer):
#     # This allows the API to return the items list inside the Order object
#     items = PurchaseOrderItemSerializer(many=True, read_only=True)
#     supplier_name = serializers.ReadOnlyField(source='supplier.name')
#     warehouse_name = serializers.ReadOnlyField(source='destination_store.name')

#     class Meta:
#         model = PurchaseOrder
#         fields = ['id','tracker', 'supplier', 'supplier_name', 'destination_store', 'warehouse_name', 'order_date', 'status', 'items']
#         read_only_fields = ['tracker', 'order_date']

# # Specialized Serializer for the Add Item logic
# class AddPurchaseItemSerializer(serializers.Serializer):
#     supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all())
#     warehouse = serializers.PrimaryKeyRelatedField(queryset=apps.get_model('inventory', 'Warehouse').objects.all())
#     product = serializers.PrimaryKeyRelatedField(queryset=apps.get_model('inventory', 'Product').objects.all())
#     quantity = serializers.IntegerField(min_value=1)
#     unit_price = serializers.DecimalField(max_digits=12, decimal_places=2)

from rest_framework import serializers
from django.apps import apps
from .models import Supplier, PurchaseOrder, PurchaseOrderItem, GoodsReceivingNote

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = [
            'id', 'tracker', 'name', 'contact_person', 
            'phone', 'email', 'address', 'status'
        ]
        read_only_fields = ['tracker']

class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    # Fetching related names for the UI
    product_name = serializers.ReadOnlyField(source='product.name')
    category_name = serializers.ReadOnlyField(source='product.category.name')
    
    class Meta:
        model = PurchaseOrderItem
        fields = [
            'id', 'tracker', 'purchase_order', 'product', 
            'product_name', 'category_name', 'quantity', 
            'unit_price', 'line_total', 'status'
        ]
        read_only_fields = ['tracker', 'line_total']

class PurchaseOrderSerializer(serializers.ModelSerializer):
    # Nested items list for the "Detail" view
    items = PurchaseOrderItemSerializer(many=True, read_only=True)
    supplier_name = serializers.ReadOnlyField(source='supplier.name')
    warehouse_name = serializers.ReadOnlyField(source='destination_store.name')
    
    # Summary fields
    item_count = serializers.SerializerMethodField()

    class Meta:
        model = PurchaseOrder
        fields = [
            'id', 'tracker', 'supplier', 'supplier_name', 
            'destination_store', 'warehouse_name', 'order_date', 
            'status', 'total_amount', 'item_count', 'items'
        ]
        read_only_fields = ['tracker', 'order_date', 'total_amount']

    def get_item_count(self, obj):
        return obj.items.count()

# --- SPECIALIZED ACTION SERIALIZER ---

class AddPurchaseItemSerializer(serializers.Serializer):
    """
    This serializer is used specifically for the 'create' action 
    to trigger the custom Manager logic.
    """
    supplier = serializers.PrimaryKeyRelatedField(
        queryset=Supplier.objects.all()
    )
    warehouse = serializers.PrimaryKeyRelatedField(
        queryset=apps.get_model('inventory', 'Warehouse').objects.all()
    )
    product = serializers.PrimaryKeyRelatedField(
        queryset=apps.get_model('inventory', 'Product').objects.all()
    )
    quantity = serializers.IntegerField(min_value=1)
    unit_price = serializers.DecimalField(max_digits=12, decimal_places=2)
    
    # This matches your requirement for "unless intentionally required 
    # to have different order number"
    force_new_order = serializers.BooleanField(default=False, required=False)

    def validate(self, data):
        # Example validation: Ensure supplier is active
        if data['supplier'].status != 'active':
            raise serializers.ValidationError("Cannot create orders for inactive suppliers.")
        return data

class GRNSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsReceivingNote
        fields = '__all__'
        read_only_fields = ['tracker', 'received_date']