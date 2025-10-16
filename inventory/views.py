from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Warehouse, ProductPackage, Product, Stock, InventoryMovementLog,StockTransfer
from .serializers import (
    WarehouseSerializer, ProductPackageSerializer, ProductSerializer,
    StockSerializer, InventoryMovementSerializer,StockTransferSerializer
)
from rest_framework.decorators import action

class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated]

class ProductPackageViewSet(viewsets.ModelViewSet):
    queryset = ProductPackage.objects.all()
    serializer_class = ProductPackageSerializer
    permission_classes = [IsAuthenticated]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated]

class InventoryMovementViewSet(viewsets.ModelViewSet):
    queryset = InventoryMovementLog.objects.all()
    serializer_class = InventoryMovementSerializer
    permission_classes = [IsAuthenticated]
# class StockTransferViewSet(viewsets.ModelViewSet):
#     queryset = StockTransfer.objects.all()
#     serializer_class = StockTransferSerializer
#     permission_classes = [IsAuthenticated]
# views.py


class StockTransferViewSet(viewsets.ModelViewSet):
    queryset = StockTransfer.objects.all().order_by('-created_at')
    serializer_class = StockTransferSerializer

    def update(self, request, *args, **kwargs):
        transfer = self.get_object()
        if transfer.status != "PENDING":
            return Response(
                {"detail": "Only pending transfers can be updated."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def authorize(self, request, pk=None):
        transfer = self.get_object()
        if transfer.status != "PENDING":
            return Response({"detail": "Only pending transfers can be authorized."}, status=400)
        transfer.status = "IN_PROGRESS"
        transfer.save()
        return Response({"detail": "Transfer authorized."}, status=200)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        transfer = self.get_object()
        if transfer.status != "IN_PROGRESS":
            return Response({"detail": "Only in-progress transfers can be completed."}, status=400)
        transfer.status = "COMPLETED"
        transfer.save()
        return Response({"detail": "Transfer completed successfully."}, status=200)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        transfer = self.get_object()
        if transfer.status not in ["PENDING", "IN_PROGRESS"]:
            return Response({"detail": "Only pending or in-progress transfers can be cancelled."}, status=400)
        transfer.status = "CANCELLED"
        transfer.save()
        return Response({"detail": "Transfer cancelled and stock restored."}, status=200)
