from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from .serializers import AddSalesItemSerializer, CustomerSerializer, SalesItemSerializer, SalesOrderSerializer, SalesTransactionSerializer
from .models import Customer, SalesOrder, SalesItem, SalesTransaction
# from .serializers import (
#     CustomerSerializer, SalesOrderSerializer, 
#     SalesItemSerializer, SalesTransactionSerializer, AddSalesItemSerializer
# )

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('-id')
    serializer_class = CustomerSerializer
    lookup_field = 'tracker'

class SalesOrderViewSet(viewsets.ModelViewSet):
    queryset = SalesOrder.objects.all().prefetch_related('items__product_name').order_by('-order_date')
    serializer_class = SalesOrderSerializer
    lookup_field = 'tracker'

class SalesItemViewSet(viewsets.ModelViewSet):
    queryset = SalesItem.objects.all().select_related('product_name', 'source_whouse')
    serializer_class = SalesItemSerializer
    lookup_field = 'tracker'

    def create(self, request, *args, **kwargs):
        """
        Custom Create: Intercepts the POST request to use Manager logic.
        This handles Order auto-creation and Item merging.
        """
        serializer = AddSalesItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            # Use the custom manager method from your models.py
            item = SalesItem.objects.create_sale_item(
                customer=serializer.validated_data['customer'],
                product=serializer.validated_data['product'],
                warehouse=serializer.validated_data['warehouse'],
                quantity=serializer.validated_data['quantity'],
                price=serializer.validated_data['price']
            )
            
            # Return the full serialized item (including the Order ID it was added to)
            output_serializer = SalesItemSerializer(item)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({"error": str(e.message)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SalesTransactionViewSet(viewsets.ModelViewSet):
    queryset = SalesTransaction.objects.all()
    serializer_class = SalesTransactionSerializer
    lookup_field = 'tracker'