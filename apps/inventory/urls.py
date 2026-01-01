from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    WarehouseViewSet,  ProductViewSet,
    StockViewSet, InventoryMovementViewSet,StockTransferViewSet
)

router = DefaultRouter()
router.register(r'warehouses', WarehouseViewSet)
# router.register(r'product-packages', ProductPa)
router.register(r'products', ProductViewSet)
router.register(r'stocks', StockViewSet)
router.register(r'inventory-movements', InventoryMovementViewSet)
router.register(r'stock-transfers', StockTransferViewSet)   

urlpatterns = [
    path('', include(router.urls)),
]
