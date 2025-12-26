from django.shortcuts import render
from rest_framework.response import Response  # ✅ correct
from rest_framework import status
from rest_framework import viewsets


from apps.inventory.models import Stock
from .models import SalesOrder,SalesItem
from .Serializer import SalesItemSerializer,SalesOrderSerializer
from .Serializer import SalesOrderSerializer


class SalesOrderViewSet(viewsets.ModelViewSet):
    queryset = SalesOrder.objects.all()
    serializer_class = SalesOrderSerializer
    def get_queryset(self):
        # Single query join with Customer table
        return (
            SalesOrder.objects
            .select_related('customer')
            .order_by('order_date')  # recent orders first
        )

# class SalesItemViewSet(viewsets.ModelViewSet):
#     queryset = SalesItem.objects.all()
#     serializer_class = SalesItemSerializer
# class SalesItemViewSet(viewsets.ModelViewSet):
#     queryset = SalesItem.objects.all().select_related(
#         'sale_order', 'product_name', 'source_whouse', 'inventory'
#     )
#     serializer_class = SalesItemSerializer

#     def create(self, request, *args, **kwargs):
#         product_name = request.data.get("product_name")
#         source_whouse = request.data.get("source_whouse")
#         quantity = int(request.data.get("quantity", 0))

#         # Get inventory record once
#         inventory_record = Stock.objects.filter(product=product_name, warehouse=source_whouse).first()
#         if not inventory_record:
#             return Response(
#                 {"detail": "No inventory record found for the specified product and warehouse."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         if inventory_record.quantity < quantity:
#             return Response(
#                 {"detail": "Insufficient stock.", "available_quantity": inventory_record.quantity},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # prepare and validate serializer data
#         data = request.data.copy()
#         serializer = self.get_serializer(data=data)
#         serializer.is_valid(raise_exception=True)

#         # Save new SalesItem, let model handle merging logic
#         sales_item = SalesItem(**serializer.validated_data)
#         result = sales_item.save()  # model handles merging logic and response message

#         # If the model returned a dict instead of saving (merged/updated)
#         if isinstance(result, dict):
#             return Response(result, status=status.HTTP_200_OK)

#         # assign inventory and save
#         sales_item.inventory = inventory_record
#         sales_item.save()

#         # return full info as JSON array
#         full_data = self.get_serializer(sales_item).data
#         return Response([full_data], status=status.HTTP_200_OK)

#     def list(self, request, *args, **kwargs):
#         """Show all items with related objects"""
#         queryset = self.get_queryset()
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, *args, **kwargs):
#         """Show full details for a specific item"""
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)
class SalesItemViewSet(viewsets.ModelViewSet):
    queryset = SalesItem.objects.all().select_related(
        'sale_order', 'product_name', 'source_whouse', 'inventory'
    )
    serializer_class = SalesItemSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Let the model handle logic and return its message or instance
        sales_item = SalesItem(**serializer.validated_data)
        result = sales_item.save()

        # If the model returned a dict (like merged or insufficient stock)
        if isinstance(result, dict):
            return Response(result, status=status.HTTP_200_OK)

        # If save() returned normally, reload from DB for full info
        full_instance = SalesItem.objects.get(pk=sales_item.pk)
        full_serializer = self.get_serializer(full_instance)
        return Response([full_serializer.data], status=status.HTTP_200_OK)
