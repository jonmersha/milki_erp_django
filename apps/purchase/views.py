from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Supplier, PurchaseOrder, PurchaseOrderItem
from .serializers import (
    SupplierSerializer, PurchaseOrderSerializer, 
    PurchaseOrderItemSerializer, AddPurchaseItemSerializer
)

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    lookup_field = 'tracker'

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    # Use prefetch_related to load items efficiently in one query
    queryset = PurchaseOrder.objects.all().prefetch_related('items')
    serializer_class = PurchaseOrderSerializer
    lookup_field = 'tracker'

class PurchaseOrderItemViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrderItem.objects.all()
    serializer_class = PurchaseOrderItemSerializer
    lookup_field = 'tracker'

    def create(self, request, *args, **kwargs):
        """
        Overrides the default create to use the Manager logic
        defined inside the PurchaseOrder model.
        """
        serializer = AddPurchaseItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Utilize the manager method inside models.py
        item = PurchaseOrder.objects.add_item_to_order(
            supplier=serializer.validated_data['supplier'],
            warehouse=serializer.validated_data['warehouse'],
            product=serializer.validated_data['product'],
            quantity=serializer.validated_data['quantity'],
            unit_price=serializer.validated_data['unit_price']
        )
        
        output_serializer = PurchaseOrderItemSerializer(item)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)