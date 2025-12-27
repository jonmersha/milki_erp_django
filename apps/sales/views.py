from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import SalesItem, SalesOrder, Customer, SalesTransaction
from .Serializer import CustomerSerializer, SalesItemSerializer, SalesOrderSerializer, AddSalesItemSerializer, SalesTransactionSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Customers to be viewed or edited.
    """
    queryset = Customer.objects.all().order_by('-created_at')
    serializer_class = CustomerSerializer
    
    # Adding search and filter capabilities
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['name', 'email', 'phone', 'id']
    ordering_fields = ['created_at', 'name']

class SalesOrderViewSet(viewsets.ModelViewSet):
    queryset = SalesOrder.objects.all().prefetch_related('items__product_name', 'customer')
    serializer_class = SalesOrderSerializer

    @action(detail=False, methods=['post'], url_path='add-item')
    def add_item(self, request):
        serializer = AddSalesItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        v_data = serializer.validated_data

        try:
            # 1. Create order if it doesn't exist
            order_id = v_data.get('sale_order').id if v_data.get('sale_order') else None
            
            if not order_id:
                if not v_data.get('customer'):
                    return Response({"error": "Customer required for new orders"}, status=400)
                new_order = SalesOrder.objects.create(customer=v_data['customer'])
                order_id = new_order.id

            # 2. Add item via Manager
            SalesOrder.objects.add_item(
                sale_order_id=order_id,
                product=v_data['product'],
                warehouse=v_data['warehouse'],
                quantity=v_data['quantity'],
                price=v_data['price']
            )

            # 3. Return full order details
            result = SalesOrder.objects.get(id=order_id)
            return Response(SalesOrderSerializer(result).data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class SalesItemViewSet(viewsets.ModelViewSet):
    queryset = SalesItem.objects.all().select_related('product_name', 'source_whouse')
    serializer_class = SalesItemSerializer

class SalesTransactionViewSet(viewsets.ModelViewSet):
    queryset = SalesTransaction.objects.all().select_related(
        'sale_item__product_name', 
        'sale_item__sale_order'
    )
    serializer_class = SalesTransactionSerializer
    filterset_fields = ['payment_status', 'payment_method', 'sale_item']
    search_fields = ['bank_reference', 'id', 'sale_item__id']

    def perform_create(self, serializer):
        # Save the transaction
        transaction = serializer.save()
        
        # Logic: If amount is paid, update the SalesItem status
        # This is a basic version; you can expand this for partial payments.
        item = transaction.sale_item
        if transaction.payment_status == 'Paid':
            item.payment_status = 'Paid'
            item.save(update_fields=['payment_status'])