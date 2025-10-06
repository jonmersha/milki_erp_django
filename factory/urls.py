# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from rest_framework_nested import routers
# from . import views

# # Main routers
# router = DefaultRouter()
# router.register('customers', views.CustomerViewSet)
# router.register('companies', views.CompanyViewSet)
# router.register('factories', views.FactoryViewSet)
# router.register('warehouses', views.WarehouseViewSet)
# router.register('categories', views.CategoryViewSet)
# router.register('products', views.ProductViewSet)
# router.register('stocks', views.StockViewSet)
# router.register('stock-movements', views.StockMovementLogViewSet)
# router.register('suppliers', views.SupplierViewSet)
# router.register('purchase-orders', views.PurchaseOrderViewSet)
# router.register('sales-orders', views.SalesOrderViewSet)
# router.register('invoices', views.InvoiceViewSet)
# router.register('payment-methods', views.PaymentMethodViewSet)
# router.register('payments', views.PaymentViewSet)
# router.register('product-stocks', views.ProductStockViewSet, basename='product-stock')

# # Nested routers
# purchase_order_router = routers.NestedDefaultRouter(router, 'purchase-orders', lookup='purchase_order')
# purchase_order_router.register('items', views.PurchaseOrderItemViewSet, basename='purchaseorder-items')

# sales_order_router = routers.NestedDefaultRouter(router, 'sales-orders', lookup='sales_order')
# sales_order_router.register('items', views.SalesOrderItemViewSet, basename='salesorder-items')

# invoice_router = routers.NestedDefaultRouter(router, 'invoices', lookup='invoice')
# invoice_router.register('items', views.InvoiceItemViewSet, basename='invoice-items')


# urlpatterns = [
#     path('', include(router.urls)),
#     path('', include(purchase_order_router.urls)),
#     path('', include(sales_order_router.urls)),
#     path('', include(invoice_router.urls)),
#     path('product-stocks/', views.ProductStockView.as_view(), name='product-stocks'),

# ]
