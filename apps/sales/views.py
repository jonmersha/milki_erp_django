from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Sum, F
from django.db import transaction

from .models import Customer, SalesOrder, SalesItem, SalesTransaction
from .serializers import (
    CustomerSerializer, 
    SalesOrderSerializer, 
    SalesItemSerializer, 
    AddSalesItemSerializer,
    SalesTransactionSerializer
)

class CustomerViewSet(viewsets.ModelViewSet):
    """
    Handles Customer CRUD.
    """
    queryset = Customer.objects.all().order_by('-id')
    serializer_class = CustomerSerializer
    lookup_field = 'tracker'


class SalesOrderViewSet(viewsets.ModelViewSet):
    """
    Manages Sales Orders with optimized queries for nested items.
    """
    queryset = SalesOrder.objects.all().select_related('customer').prefetch_related(
        'items__product_name', 
        'items__source_whouse'
    ).order_by('-order_date')
    serializer_class = SalesOrderSerializer
    lookup_field = 'tracker'

    @action(detail=True, methods=['post'])
    def confirm_order(self, request, tracker=None):
        """Custom action to move an order to Confirmed status."""
        order = self.get_object()
        if order.order_status != 'Pending':
            return Response(
                {"error": "Only pending sales can be confirmed."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.order_status = 'Confirmed'
        order.save()
        return Response({"status": "Order confirmed successfully"})


class SalesItemViewSet(viewsets.ModelViewSet):
    """
    Handles Sales Items.
    Utilizes AddSalesItemSerializer for creation to trigger Manager logic.
    """
    queryset = SalesItem.objects.all().select_related(
        'product_name', 
        'sale_order', 
        'source_whouse'
    )
    serializer_class = SalesItemSerializer
    lookup_field = 'tracker'

    def get_serializer_class(self):
        """
        Switch to AddSalesItemSerializer for POST requests to handle 
        the flattened logic required by the Manager.
        """
        if self.action == 'create':
            return AddSalesItemSerializer
        return SalesItemSerializer
    # Inside SalesItemViewSet
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            # CHANGE THIS LINE: 
            # From: SalesOrder.objects.add_item_to_order(...)
            # To: SalesItem.objects.create_sale_item(...)
            item = SalesItem.objects.create_sale_item(
                customer=serializer.validated_data['customer'],
                product=serializer.validated_data['product'],
                warehouse=serializer.validated_data['warehouse'],
                quantity=serializer.validated_data['quantity'],
                price=serializer.validated_data['price']
                # Note: ensure parameters match your create_sale_item signature
            )

            output_serializer = SalesItemSerializer(item)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # def create(self, request, *args, **kwargs):
    #     """
    #     Custom Create implementation:
    #     1. Validates via AddSalesItemSerializer.
    #     2. Calls the Manager method to handle Stock Check and Merging.
    #     3. Returns data using the standard SalesItemSerializer.
    #     """
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)

    #     try:
    #         # Trigger our custom Manager logic (SalesOrder.objects.add_item_to_order)
    #         item = SalesOrder.objects.add_item_to_order(
    #             customer=serializer.validated_data['customer'],
    #             warehouse=serializer.validated_data['warehouse'],
    #             product=serializer.validated_data['product'],
    #             quantity=serializer.validated_data['quantity'],
    #             price=serializer.validated_data['price'],
    #             force_new=serializer.validated_data.get('force_new_order', False)
    #         )

    #         # Return the resulting item using the UI-friendly serializer
    #         output_serializer = SalesItemSerializer(item)
    #         return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    #     except Exception as e:
    #         # Captures Stock validation errors or other logic failures
    #         return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance):
        """
        Optional: Add stock reconciliation here if you want to 
        return stock to inventory when an item is deleted.
        """
        with transaction.atomic():
            # If your model has a stock reconciliation method, call it here
            instance.delete()
class SalesTransactionViewSet(viewsets.ModelViewSet):
    queryset = SalesTransaction.objects.all().select_related('sale_item__product_name').order_by('-transaction_date')
    serializer_class = SalesTransactionSerializer
    lookup_field = 'tracker'

    def perform_create(self, serializer):
        """
        Custom logic during creation: automatically update the 
        payment status of the related SalesItem if needed.
        """
        with transaction.atomic():
            txn = serializer.save()
            # Logic example: If amount is fully paid, update item status
            if txn.amount >= txn.sale_item.total_price:
                txn.payment_status = 'Paid'
                txn.save()

    @action(detail=True, methods=['post'])
    def confirm_payment(self, request, tracker=None):
        """Custom endpoint to verify bank reference and mark as Paid."""
        transaction_record = self.get_object()
        transaction_record.payment_status = 'Paid'
        transaction_record.save()
        return Response({"status": "Payment confirmed"})