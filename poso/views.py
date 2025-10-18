from django.forms import ValidationError
from rest_framework import viewsets,status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import (
    Supplier, 
    
Customer,
    PurchaseOrder, PurchaseOrderItem,
    SalesOrder, SalesOrderItem,
    Payment, Invoice
)
from .serializers import (
    SupplierSerializer, 
    CustomerSerializer,
    PurchaseOrderSerializer, 
    PurchaseOrderItemSerializer,
    SalesOrderSerializer, 
    SalesOrderItemSerializer,
    PaymentSerializer, 
    InvoiceSerializer
)
from django.db import transaction

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAuthenticated]





class SalesOrderViewSet(viewsets.ModelViewSet):
    queryset = SalesOrder.objects.all()
    serializer_class = SalesOrderSerializer
    permission_classes = [IsAuthenticated]


# class SalesOrderItemViewSet(viewsets.ModelViewSet):
#     queryset = SalesOrderItem.objects.all()
#     serializer_class = SalesOrderItemSerializer
#     permission_classes = [IsAuthenticated]

# class SalesOrderItemViewSet(viewsets.ModelViewSet):
#     queryset = SalesOrderItem.objects.all()
#     serializer_class = SalesOrderItemSerializer
#     permission_classes = [IsAuthenticated]

#     def create(self, request, *args, **kwargs):
#         with transaction.atomic():
#             serializer = self.get_serializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             item = serializer.save()
#             return Response(self.get_serializer(item).data, status=status.HTTP_201_CREATED)

#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()

#         # Only pending or confirmed items can be updated
#         if instance.status in ["DELIVERED"]:
#             return Response(
#                 {"detail": "Cannot update items that are already delivered."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         with transaction.atomic():
#             serializer = self.get_serializer(instance, data=request.data, partial=True)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response(serializer.data)


class SalesOrderItemViewSet(viewsets.ModelViewSet):
    queryset = SalesOrderItem.objects.all().select_related("sales_order", "product")
    serializer_class = SalesOrderItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Create item and apply model-level stock logic."""
        sales_order = serializer.validated_data["sales_order"]
        product = serializer.validated_data["product"]

        if SalesOrderItem.objects.filter(sales_order=sales_order, product=product).exists():
            raise ValidationError("This product already exists in the sales order.")

        serializer.save()

    def perform_update(self, serializer):
        """Update item safely."""
        instance = self.get_object()
        if instance.status not in ["PENDING", "CONFIRMED"]:
            raise ValidationError("Only PENDING or CONFIRMED items can be updated.")
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        """Cancel the item, not delete it."""
        instance = self.get_object()
        if instance.status not in ["PENDING", "CONFIRMED"]:
            return Response(
                {"detail": "Only PENDING or CONFIRMED items can be cancelled."},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            instance.process_cancellation()
            instance.save(update_fields=["status"])
        return Response({"detail": "Sales Order Item cancelled successfully."}, status=status.HTTP_200_OK)



class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]
    
# class PurchaseOrderItemViewSet(viewsets.ModelViewSet):
#     queryset = PurchaseOrderItem.objects.all()
#     serializer_class = PurchaseOrderItemSerializer
#     permission_classes = [IsAuthenticated]

#     def create(self, request, *args, **kwargs):
#         data = request.data
#         purchase_order_id = data.get("purchase_order")
#         product_id = data.get("product")

#         with transaction.atomic():
#             # --- Check for duplicate ---
#             duplicate = PurchaseOrderItem.objects.select_for_update().filter(
#                 purchase_order_id=purchase_order_id,
#                 product_id=product_id
#             ).first()

#             if duplicate:
#                 # Merge quantity and update unit price
#                 duplicate.quantity += int(data.get("quantity", 0))
#                 duplicate.unit_price = data.get("unit_price", duplicate.unit_price)
#                 # Update status to 'received' if needed
#                 if data.get("status") == "received":
#                     duplicate.status = "received"
#                 duplicate.save(update_fields=['quantity', 'unit_price', 'status'])
                
#                 serializer = self.get_serializer(duplicate)
#                 return Response(serializer.data, status=status.HTTP_200_OK)

#             # --- No duplicate: create new item ---
#             return super().create(request, *args, **kwargs)

#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         data = request.data

#         with transaction.atomic():
#             # Prevent changing a received item back
#             if instance.status == "received" and data.get("status") != "received":
#                 return Response(
#                     {"detail": "Cannot revert a received item to another status."},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             # Update fields
#             instance.quantity = data.get("quantity", instance.quantity)
#             instance.unit_price = data.get("unit_price", instance.unit_price)
#             instance.status = data.get("status", instance.status)
#             instance.save()

#             serializer = self.get_serializer(instance)
#             return Response(serializer.data)
# class PurchaseOrderItemViewSet(viewsets.ModelViewSet):
#     queryset = PurchaseOrderItem.objects.all()
#     serializer_class = PurchaseOrderItemSerializer
#     permission_classes = [IsAuthenticated]

#     def create(self, request, *args, **kwargs):
#         data = request.data
#         purchase_order_id = data.get("purchase_order")
#         product_id = data.get("product")

#         with transaction.atomic():
#             duplicate = PurchaseOrderItem.objects.select_for_update().filter(
#                 purchase_order_id=purchase_order_id,
#                 product_id=product_id
#             ).first()

#             if duplicate:
#                 if duplicate.status == "pending":
#                     duplicate.quantity += int(data.get("quantity", 0))
#                     duplicate.unit_price = data.get("unit_price", duplicate.unit_price)
#                     if data.get("status") == "received":
#                         duplicate.status = "received"
#                     duplicate.save(update_fields=['quantity', 'unit_price', 'status'])
#                     serializer = self.get_serializer(duplicate)
#                     return Response(serializer.data, status=status.HTTP_200_OK)
#                 elif duplicate.status == "received":
#                     return Response(
#                         {
#                             "detail": f"Item '{duplicate.product.name}' already received. "
#                                       "Please create a new purchase order for additional quantity."
#                         },
#                         status=status.HTTP_400_BAD_REQUEST
#                     )

#             return super().create(request, *args, **kwargs)

#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()

#         if instance.status == "received":
#             return Response(
#                 {"detail": "Cannot update an item that has been received. Please create a new purchase order."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         with transaction.atomic():
#             data = request.data
#             instance.quantity = int(data.get("quantity", instance.quantity))
#             instance.unit_price = data.get("unit_price", instance.unit_price)
#             instance.status = data.get("status", instance.status)
#             instance.save()

#             serializer = self.get_serializer(instance)
#             return Response(serializer.data)
class PurchaseOrderItemViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrderItem.objects.all()
    serializer_class = PurchaseOrderItemSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            item = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Prevent updating received items
        if instance.status == "received":
            return Response(
                {"detail": "Cannot update an item that has been received. Please create a new purchase order."},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)