# from rest_framework import viewsets, status
# from rest_framework.response import Response
# from .models import Supplier, PurchaseOrder, PurchaseOrderItem
# from .serializers import (
#     SupplierSerializer, PurchaseOrderSerializer, 
#     PurchaseOrderItemSerializer, AddPurchaseItemSerializer
# )

# class SupplierViewSet(viewsets.ModelViewSet):
#     queryset = Supplier.objects.all()
#     serializer_class = SupplierSerializer
#     lookup_field = 'tracker'

# class PurchaseOrderViewSet(viewsets.ModelViewSet):
#     # Use prefetch_related to load items efficiently in one query
#     queryset = PurchaseOrder.objects.all().prefetch_related('items')
#     serializer_class = PurchaseOrderSerializer
#     lookup_field = 'tracker'

# class PurchaseOrderItemViewSet(viewsets.ModelViewSet):
#     queryset = PurchaseOrderItem.objects.all()
#     serializer_class = PurchaseOrderItemSerializer
#     lookup_field = 'tracker'

#     def create(self, request, *args, **kwargs):
#         """
#         Overrides the default create to use the Manager logic
#         defined inside the PurchaseOrder model.
#         """
#         serializer = AddPurchaseItemSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         # Utilize the manager method inside models.py
#         item = PurchaseOrder.objects.add_item_to_order(
#             supplier=serializer.validated_data['supplier'],
#             warehouse=serializer.validated_data['warehouse'],
#             product=serializer.validated_data['product'],
#             quantity=serializer.validated_data['quantity'],
#             unit_price=serializer.validated_data['unit_price']
#         )
        
#         output_serializer = PurchaseOrderItemSerializer(item)
#         return Response(output_serializer.data, status=status.HTTP_201_CREATED)

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Sum, F
from .models import Supplier, PurchaseOrder, PurchaseOrderItem, GoodsReceivingNote
from .serializers import (
    SupplierSerializer, PurchaseOrderSerializer, 
    PurchaseOrderItemSerializer, AddPurchaseItemSerializer,
    GRNSerializer
)

class SupplierViewSet(viewsets.ModelViewSet):
    """
    Standard CRUD for Suppliers.
    """
    queryset = Supplier.objects.all().order_by('-id')
    serializer_class = SupplierSerializer
    lookup_field = 'tracker'


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    """
    Manages Purchase Orders. 
    Uses prefetch_related for high performance when loading nested items.
    """
    queryset = PurchaseOrder.objects.all().prefetch_related('items').order_by('-order_date')
    serializer_class = PurchaseOrderSerializer
    lookup_field = 'tracker'

    @action(detail=True, methods=['post'])
    def confirm_order(self, request, tracker=None):
        """Custom action to move an order from Pending to Confirmed."""
        order = self.get_object()
        if order.status != 'Pending':
            return Response({"error": "Only pending orders can be confirmed."}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = 'Confirmed'
        order.save()
        return Response({"status": "Order confirmed successfully"})


class PurchaseOrderItemViewSet(viewsets.ModelViewSet):
    """
    Handles individual items within orders.
    Overrides 'create' to implement the 'Auto-Create/Merge' logic.
    """
    queryset = PurchaseOrderItem.objects.all().select_related('product', 'purchase_order')
    serializer_class = PurchaseOrderItemSerializer
    lookup_field = 'tracker'

    def get_serializer_class(self):
        """
        Switch to the specialized 'Add' serializer for POST requests 
        to capture supplier, warehouse, and force_new_order fields.
        """
        if self.action == 'create':
            return AddPurchaseItemSerializer
        return PurchaseOrderItemSerializer

    def create(self, request, *args, **kwargs):
        """
        Custom Create:
        1. Validates input using AddPurchaseItemSerializer.
        2. Calls the Manager method to handle logic (Merge vs. New PO).
        3. Recalculates PO totals.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            # Trigger our custom Manager logic
            item = PurchaseOrder.objects.add_item_to_order(
                supplier=serializer.validated_data['supplier'],
                warehouse=serializer.validated_data['warehouse'],
                product=serializer.validated_data['product'],
                quantity=serializer.validated_data['quantity'],
                unit_price=serializer.validated_data['unit_price'],
                force_new=serializer.validated_data.get('force_new_order', False)
            )

            # Update the parent Purchase Order total amount
            # This ensures the PO reflects the sum of all its items
            order = item.purchase_order
            total = order.items.aggregate(
                total=Sum(F('quantity') * F('unit_price'))
            )['total'] or 0.00
            
            order.total_amount = total
            order.save()

            # Return the created/merged item using the standard item serializer
            output_serializer = PurchaseOrderItemSerializer(item)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GRNViewSet(viewsets.ModelViewSet):
    """
    Handles Goods Receiving Notes.
    """
    queryset = GoodsReceivingNote.objects.all().order_by('-received_date')
    serializer_class = GRNSerializer
    lookup_field = 'tracker'