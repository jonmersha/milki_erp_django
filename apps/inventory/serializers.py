from rest_framework import serializers
from .models import Warehouse, Product, Stock, InventoryMovementLog, StockTransfer

class WarehouseSerializer(serializers.ModelSerializer):
    factory_name = serializers.ReadOnlyField(source='factory.name')

    class Meta:
        model = Warehouse
        fields = [
            'tracker', 'name', 'factory', 'factory_name', 
            'location', 'capacity', 'status', 'description'
        ]
        read_only_fields = ['tracker']

class ProductSerializer(serializers.ModelSerializer):
    company_name = serializers.ReadOnlyField(source='company.name')

    class Meta:
        model = Product
        fields = [
            'tracker', 'name', 'unit_price', 'unit_of_measure', 
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