
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
# from rest_framework.documentation import include_docs_urls  # Enable if needed

from main.cd import CreateAdminUserView

# CORE
from apps.core.views import (
    CityViewSet, CompanyViewSet, FactoryViewSet, AdminRegionViewSet
)

# SALES (replacing POSO)
from main.views import FrontendAppView
from apps.sales.views import CustomerViewSet, SalesOrderViewSet, SalesItemViewSet, SalesTransactionViewSet
# PURCHASE
from apps.purchase.views import PurchaseOrderViewSet, PurchaseOrderItemViewSet, SupplierViewSet
    
# INVENTORY
from apps.inventory.views import (
    WarehouseViewSet,  ProductViewSet,
    StockViewSet, InventoryMovementViewSet, StockTransferViewSet
)

# USERS
from apps.users.views import UserViewSet

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# -----------------------------
# Admin UI Branding
# -----------------------------
admin.site.site_header = "Milki System Administration"
admin.site.site_title = "Milki Admin Portal"
admin.site.index_title = "Welcome to Milki Management Dashboard"

# -----------------------------
# Routers (modular per app)
# -----------------------------
core_router = DefaultRouter()
inventory_router = DefaultRouter()
users_router = DefaultRouter()
sales_router = DefaultRouter()

# CORE routes
core_router.register(r'companies', CompanyViewSet)
core_router.register(r'factories', FactoryViewSet)
core_router.register(r'admin-regions', AdminRegionViewSet)
core_router.register(r'cities', CityViewSet)


# SALES routes
sales_router.register(r'orders', SalesOrderViewSet, basename='sales-orders')
sales_router.register(r'order-items', SalesItemViewSet, basename='sales-order-items')
sales_router.register(r'customers', CustomerViewSet, basename='customer')
sales_router.register(r'sales-transactions', SalesTransactionViewSet, basename='sales-transactions')
# PURCHASE routes
purchase_router = DefaultRouter()
purchase_router.register(r'orders', PurchaseOrderViewSet, basename='purchase-orders')
purchase_router.register(r'order-items', PurchaseOrderItemViewSet, basename='purchase-order-items')
purchase_router.register(r'suppliers', SupplierViewSet, basename='suppliers')
# #godds receiving notes
# goods_router = DefaultRouter()
# goods_router.register(r'grns', GoodsReceivingNoteViewSet, basename='grns')
# goods_router.register(r'grn-items', GRNItemViewSet, basename='grn-items')

# INVENTORY routes
inventory_router.register(r'warehouses', WarehouseViewSet)
# inventory_router.register(r'product-packages', ProductPackageViewSet)
inventory_router.register(r'products', ProductViewSet)
inventory_router.register(r'stocks', StockViewSet)
inventory_router.register(r'inventory-movements', InventoryMovementViewSet)
inventory_router.register(r'stock-transfers', StockTransferViewSet, basename='stock-transfers')

# USERS routes
users_router.register(r'users', UserViewSet)

# -----------------------------
# URL Patterns
# -----------------------------
urlpatterns = [
    
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # 2. This view is the UI that reads the schema above
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    #  path('', home_view, name='home'),
    # Admin panel
    path('admin/', admin.site.urls),
    # Auth (Djoser)
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    # Create super admin (custom endpoint)
    path('cd/', CreateAdminUserView.as_view(), name="create-admin"),

    # API Groups
    path('core/', include(core_router.urls)),           # /core/companies/
    path('sales/', include(sales_router.urls)),         # /sales/orders/
    path('purchase/', include(purchase_router.urls)),   # /purchase/orders/
    path('inventory/', include(inventory_router.urls)), # /inventory/products/
    path('users/', include(users_router.urls)),         # /users/users/

    # Schema (OpenAPI)
    path(
        'api/schema/',
        get_schema_view(
            title="Milki System API",
            description="Centralized ERP API Schema",
            version="1.0.0"
        ),
        name='openapi-schema'
    ),

#     # API Docs (enable when needed)
#     # path('api/docs/', include_docs_urls(title="Milki System API Docs")),
#     # Catch-all pattern to serve React app
#     # re_path(r'^.*$', FrontendAppView.as_view(), name='home'),
#     # re_path(r'^sw$', ServiceWorkerView.as_view(), name='service-worker'),
# # 1. Download the schema (YAML/JSON)
#    # The view that generates the schema
#     path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
#     # The UI view
#     path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
#     # 3. Redoc UI (Optional):
#     # path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

]
urlpatterns += staticfiles_urlpatterns()  
# urlpatterns += staticfiles_urlpatterns()
# Media handling (development only)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
