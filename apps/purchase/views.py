from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import PurchaseOrder, PurchaseOrderItem, Supplier
from .serializer import (
    PurchaseOrderSerializer,
    SupplierSerializer, 
    PurchaseOrderItemSerializer, 
    PurchaseOrderItemSerializer,
    AddOrderItemSerializer
)

class SupplierViewSet(viewsets.ModelViewSet):
    """
    Standard CRUD for Suppliers.
    """
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status']
    search_fields = ['name', 'email']

class PurchaseOrderItemViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset to list or retrieve specific items. 
    Creation is usually handled via the PurchaseOrder 'add_item' action.
    """
    queryset = PurchaseOrderItem.objects.all()
    serializer_class = PurchaseOrderItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['purchase_order', 'product', 'status']

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all().prefetch_related('items__product', 'supplier', 'destination_store')
    # Use the ORDER serializer, not the ITEM serializer
    serializer_class = PurchaseOrderSerializer

    @action(detail=False, methods=['post'], url_path='add-item')
    def add_item(self, request):
        serializer = AddOrderItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        v_data = serializer.validated_data
        
        try:
            # Execute manager logic
            purchase_order = PurchaseOrder.objects.add_item(
                product=v_data['product'],
                quantity=v_data['quantity'],
                unit_price=v_data['unit_price'],
                supplier_id=v_data.get('supplier').id if v_data.get('supplier') else None,
                warehouse_id=v_data.get('destination_store').id if v_data.get('destination_store') else None,
                po_id=v_data.get('purchase_order').id if v_data.get('purchase_order') else None
            )

            # Return the full PO (Starts with "PO...") with nested items (Start with "POI...")
            return Response(self.get_serializer(purchase_order).data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    @action(detail=True, methods=['post'], url_path='receive-goods')
    def receive_goods(self, request, pk=None):
        """
        POST /purchase/orders/{id}/receive-goods/
        Payload: {
            "received_by": "John Doe",
            "items": [{"po_item_id": "POI...", "qty": 10}]
        }
        """
        po = self.get_object()
        if po.status == 'received':
            return Response({"error": "This PO is already fully received."}, status=400)

        try:
            grn = PurchaseOrder.objects.create_grn_from_po(
                po_id=po.id,
                received_by=request.data.get('received_by'),
                items_data=request.data.get('items', [])
            )
            return Response(GRNSerializer(grn).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)