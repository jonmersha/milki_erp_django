from rest_framework import serializers

from apps.inventory.models import Product, Warehouse
from .models import GRNItem, GoodsReceivingNote, Supplier, PurchaseOrder, PurchaseOrderItem

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = [
            'id', 
            'name', 
            'contact_person', 
            'phone', 
            'email', 
            'address', 
            'status',
            'created_at',  # Inherited from BaseModel
            'updated_at'   # Inherited from BaseModel
        ]
        # Marked as read_only because they are system-generated
        read_only_fields = ('id', 'created_at', 'updated_at')

class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = PurchaseOrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'unit_price', 'status', 'total_price']

class PurchaseOrderSerializer(serializers.ModelSerializer):
    # 'items' refers to the related_name in PurchaseOrderItem model
    items = PurchaseOrderItemSerializer(many=True, read_only=True)
    supplier_name = serializers.ReadOnlyField(source='supplier.name')
    warehouse_name = serializers.ReadOnlyField(source='destination_store.name')

    class Meta:
        model = PurchaseOrder
        fields = ['id', 'supplier', 'supplier_name', 'destination_store', 'warehouse_name', 'status', 'order_date', 'items']

class AddOrderItemSerializer(serializers.Serializer):
    purchase_order = serializers.SlugRelatedField(slug_field='id', queryset=PurchaseOrder.objects.all(), required=False, allow_null=True)
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all(), required=False)
    destination_store = serializers.PrimaryKeyRelatedField(queryset=Warehouse.objects.all(), required=False)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField(min_value=1)
    unit_price = serializers.DecimalField(max_digits=12, decimal_places=2)
    
class GRNItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='po_item.product.name')

    class Meta:
        model = GRNItem
        fields = ['id', 'po_item', 'product_name', 'quantity_received']

class GRNSerializer(serializers.ModelSerializer):
    items = GRNItemSerializer(many=True, read_only=True)

    class Meta:
        model = GoodsReceivingNote
        fields = ['id', 'purchase_order', 'received_by', 'received_date', 'items']
        read_only_fields = ['id']