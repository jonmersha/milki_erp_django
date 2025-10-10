from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Warehouse, ProductPackage, Product, Stock, InventoryMovementLog,StockTransfer
from .serializers import (
    WarehouseSerializer, ProductPackageSerializer, ProductSerializer,
    StockSerializer, InventoryMovementSerializer,StockTransferSerializer
)

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
class StockTransferViewSet(viewsets.ModelViewSet):
    queryset = StockTransfer.objects.all()
    serializer_class = StockTransferSerializer
    permission_classes = [IsAuthenticated]