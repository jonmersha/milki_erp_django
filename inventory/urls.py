from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    WarehouseViewSet, ProductPackageViewSet, ProductViewSet,
    StockViewSet, InventoryMovementViewSet
)

router = DefaultRouter()
router.register(r'warehouses', WarehouseViewSet)
router.register(r'product-packages', ProductPackageViewSet)
router.register(r'products', ProductViewSet)
router.register(r'stocks', StockViewSet)
router.register(r'inventory-movements', InventoryMovementViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
