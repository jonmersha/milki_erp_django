from rest_framework import serializers
from .models import Warehouse, ProductPackage, Product, Stock, InventoryMovementLog, StockTransfer
from django.conf import settings
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
class PRD(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id', 'name', 'description', 'unit_price']

class StockSerializer(serializers.ModelSerializer):
    d =PRD(read_only=True)
    # warehouse=WarehouseSerializer()
    class Meta:
        model = Stock
        fields = [
            'id', 'd','product', 'warehouse', 'quantity', 'last_updated',
            'remarks', 'locked_amount', 'unit_price', 'total_value',
            'minimum_threshold', 'created_at', 'updated_at'
        ]

# -----------------------------
# InventoryMovement
# -----------------------------
class InventoryMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryMovementLog
        fields = [
            'id', 'product', 'date', 'quantity', 'movement_type',
            'warehouse', 'unit_price',
            'remarks', 'status', 'created_at', 'updated_at'
        ]

class StockTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockTransfer
        fields = [
            'id', 'product', 'source_warehouse', 'destination_warehouse', 'quantity',
            'status', 'authorized_by', 'created_at', 'updated_at'
        ]   
