from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Warehouse, Product, Stock, InventoryMovementLog, StockTransfer
from .serializers import (
    WarehouseSerializer, ProductSerializer, StockSerializer, 
    InventoryMovementLogSerializer, StockTransferSerializer
)

class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    lookup_field = 'tracker'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'factory']
    search_fields = ['name', 'location']

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'tracker'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'company', 'unit_of_measure']
    search_fields = ['name', 'description']
    ordering_fields = ['unit_price', 'name']

class StockViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Note: Stock is usually updated via Purchase/Sales/Transfers, 
    so we use ReadOnlyModelViewSet to prevent manual tampering via API.
    """
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    lookup_field = 'tracker'
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['product', 'warehouse']
    ordering_fields = ['quantity', 'total_value']

class StockTransferViewSet(viewsets.ModelViewSet):
    queryset = StockTransfer.objects.all()
    serializer_class = StockTransferSerializer
    lookup_field = 'tracker'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'product', 'source_warehouse', 'destination_warehouse']

    def perform_create(self, serializer):
        # The logic inside StockTransfer.save() handles the stock locking
        serializer.save()

class InventoryMovementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InventoryMovementLog.objects.all().select_related(
        'product', 
        'source_warehouse', 
        'destination_warehouse'
    ).order_by('-date')
    
    serializer_class = InventoryMovementLogSerializer
    lookup_field = 'tracker'
    
    # Standard filtering for the Flutter app
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['product', 'movement_type', 'reason', 'source_warehouse']
    
    # Allowing the frontend to change sorting if needed
    ordering_fields = ['date', 'quantity']