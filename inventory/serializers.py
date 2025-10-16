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
            'id',
            'name',
            'description',
            'size',
            'dimensions',
            'weight',
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        return ProductPackage.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

# -----------------------------
# Product
# -----------------------------
class ProductSerializer(serializers.ModelSerializer):
    package_name = serializers.CharField(source='package.name', read_only=True)
    company_name = serializers.CharField(source='company.name', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'unit_price',
            'unit_of_measure',
            'package',
            'package_name',
            'status',
            'company',
            'company_name',
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
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

# class StockTransferSerializer(serializers.ModelSerializer):
#     product_name = serializers.CharField(source='product.name', read_only=True)
#     source_warehouse_name = serializers.CharField(source='source_warehouse.name', read_only=True)
#     destination_warehouse_name = serializers.CharField(source='destination_warehouse.name', read_only=True)

#     class Meta:
#         model = StockTransfer
#         fields = [
#             "id",
#             "product",
#             "product_name",
#             "quantity",
#             "unit_of_measure",
#             "source_warehouse",
#             "source_warehouse_name",
#             "destination_warehouse",
#             "destination_warehouse_name",
#             "status",
#             "requested_date",
#             "authorized_date",
#             "completed_date",
#             "remarks",
#         ]
#         read_only_fields = ("id", "requested_date", "authorized_date", "completed_date") 

# serializers.py


class StockTransferSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    source_warehouse_name = serializers.CharField(source="source_warehouse.name", read_only=True)
    destination_warehouse_name = serializers.CharField(source="destination_warehouse.name", read_only=True)

    class Meta:
        model = StockTransfer
        fields = [
            'id', 'product', 'product_name',
            'source_warehouse', 'source_warehouse_name',
            'destination_warehouse', 'destination_warehouse_name',
            'quantity', 'locked_amount', 'status',
            'remarks', 'created_at', 'updated_at'
        ]
        read_only_fields = ['locked_amount', 'created_at', 'updated_at']
