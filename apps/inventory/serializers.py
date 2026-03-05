from rest_framework import serializers
from .models import Warehouse, Product, Stock, InventoryMovementLog, StockTransfer

class WarehouseSerializer(serializers.ModelSerializer):
    factory_name = serializers.ReadOnlyField(source='factory.name')

    class Meta:
        model = Warehouse
        fields = [
            'id', 'tracker', 'name', 'factory', 'factory_name', 
            'location', 'capacity', 'status', 'description'
        ]
        read_only_fields = ['tracker']

class ProductSerializer(serializers.ModelSerializer):
    company_name = serializers.ReadOnlyField(source='company.name')

    class Meta:
        model = Product
        fields = [
            'id', 'tracker', 'name', 'unit_price', 'unit_of_measure', 
            'status', 'company', 'company_name', 'description'
        ]
        read_only_fields = ['tracker']

class StockSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    warehouse_name = serializers.ReadOnlyField(source='warehouse.name')
    unit_of_measure = serializers.ReadOnlyField(source='product.unit_of_measure')

    class Meta:
        model = Stock
        fields = [
            'tracker', 'product', 'product_name', 'warehouse', 
            'warehouse_name', 'quantity', 'locked_amount', 
            'unit_price', 'total_value', 'unit_of_measure'
        ]
        read_only_fields = ['tracker', 'total_value']

class InventoryMovementLogSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    source_name = serializers.ReadOnlyField(source='source_warehouse.name')
    destination_name = serializers.ReadOnlyField(source='destination_warehouse.name')

    class Meta:
        model = InventoryMovementLog
        fields = [
            'tracker', 'product', 'product_name', 'quantity', 
            'movement_type', 'reason', 'source_warehouse', 'source_name',
            'destination_warehouse', 'destination_name', 'date'
        ]
        read_only_fields = ['tracker', 'date']

class StockTransferSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    source_name = serializers.ReadOnlyField(source='source_warehouse.name')
    destination_name = serializers.ReadOnlyField(source='destination_warehouse.name')

    class Meta:
        model = StockTransfer
        fields = [
            'tracker', 'product', 'product_name', 'source_warehouse', 
            'source_name', 'destination_warehouse', 'destination_name', 
            'quantity', 'status'
        ]
        read_only_fields = ['tracker']



class StockInWarehouseSerializer(serializers.ModelSerializer):
    """
    Shows individual product levels inside a specific warehouse.
    """
    product_name = serializers.ReadOnlyField(source='product.name')
    product_unit = serializers.ReadOnlyField(source='product.unit_of_measure')
    # total_value is calculated in the model's save() method
    
    class Meta:
        model = Stock
        fields = [
            'tracker', 'product_name', 'product_unit', 
            'quantity', 'unit_price', 'total_value'
        ]

class WarehouseListSerializer(serializers.ModelSerializer):
    """
    The main serializer for the Flutter Warehouse List Page.
    """
    # This 'stocks' field matches the related_name in your Stock model
    stocks = StockInWarehouseSerializer(many=True, read_only=True)
    total_warehouse_value = serializers.SerializerMethodField()

    class Meta:
        model = Warehouse
        fields = [
            'id', 'tracker', 'name', 'location', 
            'capacity', 'status', 'stocks', 'total_warehouse_value'
        ]

    def get_total_warehouse_value(self, obj):
        # Sums up the financial value of everything in this specific building
        return sum(stock.total_value or 0 for stock in obj.stocks.all())