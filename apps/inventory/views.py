from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Warehouse, ProductPackage, Product, Stock, InventoryMovementLog,StockTransfer
from .serializers import (
    WarehouseSerializer, ProductPackageSerializer, ProductSerializer,
    StockSerializer, InventoryMovementLogSerializer,StockTransferSerializer
)
from rest_framework.decorators import action
from django.db import transaction

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
    serializer_class = InventoryMovementLogSerializer
    permission_classes = [IsAuthenticated]

class StockTransferViewSet(viewsets.ModelViewSet):
    queryset = StockTransfer.objects.all().order_by('-created_at')
    serializer_class = StockTransferSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        transfer = self.get_object()
        if transfer.status != "PENDING":
            return Response({"detail": "Only pending transfers can be completed."}, status=400)

        transfer.status = "COMPLETED"
        transfer.save()
        return Response({"detail": "Transfer completed successfully."}, status=200)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        transfer = self.get_object()

        if transfer.status == "COMPLETED":
            return Response({"detail": "Completed transfers cannot be cancelled."}, status=400)
        if transfer.status == "CANCELLED":
            return Response({"detail": "This transfer is already cancelled."}, status=400)

        transfer.status = "CANCELLED"
        transfer.save()
        return Response({"detail": "Transfer cancelled and stock restored."}, status=200)
