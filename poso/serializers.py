from rest_framework import serializers

from inventory.serializers import ProductSerializer
from .models import (
    Supplier, Customer,
    PurchaseOrder, PurchaseOrderItem,
    SalesOrder, SalesOrderItem,
    Payment, Invoice
)

# -----------------------------
# Partners
# -----------------------------
class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = [
            'id', 'name', 'contact_person', 'phone', 'email', 'address',
            'status', 'created_at', 'updated_at'
        ]


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'id', 'name', 'phone', 'email', 'address',
            'status', 'created_at', 'updated_at'
        ]


# -----------------------------
# Purchase Orders
# -----------------------------
class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = PurchaseOrderItem
        fields = [
            'id', 'purchase_order', 'product', 'quantity', 'unit_price',
            'status', 'total_price', 'created_at', 'updated_at'
        ]


class PurchaseOrderSerializer(serializers.ModelSerializer):
    items = PurchaseOrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = [
            'id', 'supplier', 'order_date', 'status',
            'created_at', 'updated_at', 'items'
        ]


# -----------------------------
# Sales Orders
# -----------------------------
class SalesOrderItemSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()
    product = ProductSerializer().read_only=True

    class Meta:
        model = SalesOrderItem
        fields = [
            'id', 'sales_order', 'product', 'quantity', 'unit_price',
            'total_price', 'created_at', 'updated_at'
        ]


class SalesOrderSerializer(serializers.ModelSerializer):
    items = SalesOrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = SalesOrder
        fields = [
            'id', 'customer', 'order_date', 'status',
            'created_at', 'updated_at', 'items'
        ]


# -----------------------------
# Payments
# -----------------------------
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id', 'sales_order', 'purchase_order', 'amount',
            'method', 'status', 'created_at', 'updated_at'
        ]


# -----------------------------
# Invoices
# -----------------------------
class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = [
            'id', 'sales_order', 'purchase_order', 'invoice_date',
            'total_amount', 'status', 'created_at', 'updated_at'
        ]
