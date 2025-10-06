from rest_framework import serializers
from .models import Warehouse, ProductPackage, Product, Stock, InventoryMovement

# -----------------------------
# Warehouse
# -----------------------------
class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = [
            'id', 'factory', 'name', 'description', 'location',
            'capacity', 'status', 'created_at', 'updated_at'
        ]

# -----------------------------
# ProductPackage
# -----------------------------
class ProductPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPackage
        fields = [
            'id', 'name', 'created_at', 'updated_at'
        ]

# -----------------------------
# Product
# -----------------------------
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'unit_price', 'unit_of_measure',
            'package_size', 'package_name', 'status', 'factory',
            'created_at', 'updated_at'
        ]

# -----------------------------
# Stock
# -----------------------------
class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = [
            'id', 'product', 'warehouse', 'quantity', 'last_updated',
            'remarks', 'locked_amount', 'unit_price', 'total_value',
            'minimum_threshold', 'created_at', 'updated_at'
        ]

# -----------------------------
# InventoryMovement
# -----------------------------
class InventoryMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryMovement
        fields = [
            'id', 'product', 'date', 'quantity', 'movement_type',
            'source_warehouse', 'destination_warehouse', 'unit_price',
            'remarks', 'status', 'created_at', 'updated_at'
        ]
