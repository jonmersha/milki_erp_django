from rest_framework import serializers
from django.contrib.auth import get_user_model
from core.serializer import UserSerializer
from .models import *
from rest_framework import generics


class CustomerSerializer(serializers.ModelSerializer):
    # Include related User fields
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    email = serializers.EmailField(source='user.email', required=False)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'phone',  'username', 'first_name', 'last_name', 'email']

    def update(self, instance, validated_data):
        # Update Customer fields
        customer_data = {k: v for k, v in validated_data.items() if k != 'user'}
        for attr, value in customer_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update related User fields
        user_data = validated_data.get('user', {})
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        return instance



# 2. Company Serializer
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'description', 'customer', 'logo_url', 'company_status', 'created_at', 'updated_at']


# 3. Factory Serializer
class FactorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Factory
        fields = ['id', 'name', 'description', 'location_name', 'city', 'admin_region', 
                  'latitude_point', 'longitude_point', 'is_operational', 'production_capacity', 
                  'is_authorized', 'authorization_time', 'created_at', 'updated_at', 'inputer', 'company']


# 4. Warehouse Serializer
class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id', 'factory','description','capacity', 'status', 'is_authorized', 'authorization_time', 
                  'created_at', 'updated_at', 'authorized_by']


# 5. Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


# 6. Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'code', 'name', 'description', 'category', 'unit_of_measure', 
                  'status', 'is_authorized', 'authorization_time', 'created_at', 'updated_at', 
                  'company', 'authorizer', 'inputer']


# 7. Stock Serializer
class StockSerializer(serializers.ModelSerializer):
    # product = ProductSerializer(read_only=True)  # Nested product serializer
    # warehouse = WarehouseSerializer(read_only=True)  # Nested warehouse serializer
    class Meta:
        model = Stock
        fields = ['id', 'warehouse', "product", 'unit_price', 'quantity', 
                  'last_updated', 'is_authorized', 'authorization_time', 'authorizer', 'inputer']
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be a positive number.")
        return value

    def validate_unit_price(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError("Unit price must be a positive number.")
        return value


# 8. Stock Movement Log Serializer
class StockMovementLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockMovementLog
        fields = ['id', 'product', 'mdate', 'unit_price', 'quantity', 'movement_type', 
                  'remarks', 'status', 'is_authorized', 'authorization_time', 'logged_at', 
                  'source_factory', 'destination_factory', 'source_warehouse', 'destination_warehouse',
                  'authorizer', 'inputer']


# 9. Supplier Serializer
class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'supplier_name', 'supplier_contact_person', 'supplier_phone', 
                  'supplier_email', 'supplier_address', 'company', 'supplier_status', 
                  'is_authorized', 'authorization_time', 'inputer', 'created_at', 'updated_at']


# 10. Purchase Order Serializer
class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['id', 'placed_at', 'supplier', 'inputer', 'authorizer', 
                  'order_status', 'payment_status', 'is_authorized', 'authorized_at']


# 11. Purchase Order Item Serializer
class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderItem
        fields = ['id', 'purchase_order', 'product', 'factory', 'warehouse', 
                  'order_date', 'supplier', 'quantity', 'unit_price', 
                  'payment_status', 'authorization_time', 'created_at', 'updated_at']


# 12. Sales Order Serializer
class SalesOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesOrder
        fields = ['id', 'placed_at', 'to_customer', 'inputer', 'authorizer', 
                  'order_status', 'payment_status', 'is_authorized', 'authorization_time']


# 13. Sales Order Item Serializer
class SalesOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesOrderItem
        fields = ['id', 'sales_order', 'product', 'quantity', 'factory', 'warehouse', 
                  'unit_price', 'total_price']


# 14. Invoice Serializer
class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id', 'invoice_number', 'invoice_type', 'sales_order', 'purchase_order', 
                  'customer', 'supplier', 'issue_date', 'due_date', 'total_amount', 
                  'tax_amount', 'discount_amount', 'status', 'created_at', 'updated_at']


# 15. Invoice Item Serializer
class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ['id', 'invoice', 'product', 'description', 'quantity', 'unit_price', 'total_price']


# 16. Payment Method Serializer
class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ['id', 'method_name', 'description']


# 17. Payment Serializer
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'invoice', 'payment_date', 'amount', 'method', 'reference_number', 
                  'payer', 'supplier', 'status', 'created_at', 'updated_at']



#========================================Products in warehouses===============================
class WarehouseStockSerializer(serializers.ModelSerializer):
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)

    class Meta:
        model = Stock
        fields = ['warehouse_name', 'quantity']

class ProductStockSerializer(serializers.ModelSerializer):
    stocks = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'code', 'name', 'description', 'stocks']

    def get_stocks(self, obj):
        # Prefetch warehouses to reduce queries
        stocks = Stock.objects.filter(product=obj).select_related('warehouse')
        return WarehouseStockSerializer(stocks, many=True).data