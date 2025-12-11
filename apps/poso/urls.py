from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    SupplierViewSet, CustomerViewSet,
    PurchaseOrderViewSet, PurchaseOrderItemViewSet,
    SalesOrderViewSet, SalesOrderItemViewSet,
    PaymentViewSet, InvoiceViewSet
)

router = DefaultRouter()
router.register(r'suppliers', SupplierViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'purchase-orders', PurchaseOrderViewSet)
router.register(r'purchase-order-items', PurchaseOrderItemViewSet)
router.register(r'sales-orders', SalesOrderViewSet)
router.register(r'sales-order-items', SalesOrderItemViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'invoices', InvoiceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
