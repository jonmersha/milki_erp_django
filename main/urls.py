# # from django.contrib import admin
# # from django.urls import path, include
# # from rest_framework.routers import DefaultRouter
# # from main.cd import CreateAdminUserView
# # from django.conf import settings
# # from django.conf.urls.static import static

# # # Import all viewsets
# # from core.views import AdminRegionViewSet, CityViewSet, CompanyViewSet, FactoryViewSet
# #   # Replace with actual viewsets
# # from poso.views import (
# #     SupplierViewSet, CustomerViewSet,
# #     PurchaseOrderViewSet, PurchaseOrderItemViewSet,
# #     SalesOrderViewSet, SalesOrderItemViewSet,
# #     PaymentViewSet, InvoiceViewSet
# # )
# # from inventory.views import (
# #     WarehouseViewSet, ProductPackageViewSet, ProductViewSet,
# #     StockViewSet, InventoryMovementViewSet
# # )

# # # -----------------------------
# # # DRF router
# # # -----------------------------
# # router = DefaultRouter()

# # # Core app viewsets
# # # router.register(r'core1', CoreViewSet1)  # Example
# # # router.register(r'core2', CoreViewSet2)

# # #CORE app viewsets
# # router.register(r'adminregions', AdminRegionViewSet, basename='adminregion')
# # router.register(r'cities', CityViewSet, basename='city')
# # router.register(r'companies', CompanyViewSet, basename='company')
# # router.register(r'factories', FactoryViewSet, basename='factory')

# # # POS app viewsets
# # router.register(r'suppliers', SupplierViewSet)
# # router.register(r'customers', CustomerViewSet)
# # router.register(r'purchase-orders', PurchaseOrderViewSet)
# # router.register(r'purchase-order-items', PurchaseOrderItemViewSet)
# # router.register(r'sales-orders', SalesOrderViewSet)
# # router.register(r'sales-order-items', SalesOrderItemViewSet)
# # router.register(r'payments', PaymentViewSet)
# # router.register(r'invoices', InvoiceViewSet)

# # # Inventory app viewsets
# # router.register(r'warehouses', WarehouseViewSet)
# # router.register(r'products', ProductViewSet)
# # router.register(r'product-packages', ProductPackageViewSet)
# # router.register(r'stocks', StockViewSet)
# # router.register(r'inventory-movements', InventoryMovementViewSet)


# # # -----------------------------
# # # URL patterns
# # # -----------------------------
# # urlpatterns = [
# #     path('admin/', admin.site.urls),
# #     path('', include(router.urls)),                 # All API endpoints at root
# #     path('auth/', include('djoser.urls')),         # Auth endpoints
# #     path('auth/', include('djoser.urls.jwt')),     # JWT endpoints
# #     path('cd/', CreateAdminUserView.as_view(), name="create-admin"),  # Admin creation
# # ]

# # # Serve media in development
# # if settings.DEBUG:
# #     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# from django.contrib import admin
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from rest_framework.schemas import get_schema_view
# from rest_framework.documentation import include_docs_urls
# from django.conf import settings
# from django.conf.urls.static import static
# from main.cd import CreateAdminUserView

# # -----------------------------
# # Import all ViewSets
# # -----------------------------
# # CORE app viewsets
# from core.views import (
#     CityViewSet, CompanyViewSet, FactoryViewSet, AdminRegionViewSet
# )

# # POSO app viewsets
# # from poso.views import (
# #     SupplierViewSet, CustomerViewSet,
# #     PurchaseOrderViewSet, PurchaseOrderItemViewSet,
# #     SalesOrderViewSet, SalesOrderItemViewSet,
# #     PaymentViewSet, InvoiceViewSet
# # )

# from sales.views import SalesOrderViewSet, SalesItemViewSet


# admin.site.site_header = "Milki System Administration"
# admin.site.site_title = "Milki Admin Portal"
# admin.site.index_title = "Welcome to Milki System Management Dashboard"

# # INVENTORY app viewsets
# from inventory.views import (
#     WarehouseViewSet, ProductPackageViewSet, ProductViewSet,
#     StockViewSet, InventoryMovementViewSet, StockTransferViewSet
# )
# from users.views import UserViewSet

# # -----------------------------
# # Routers per app
# # -----------------------------
# core_router = DefaultRouter()
# poso_router = DefaultRouter()
# inventory_router = DefaultRouter()
# users_router = DefaultRouter()
# so_router = DefaultRouter()

# # CORE routes
# core_router.register(r'companies', CompanyViewSet)
# core_router.register(r'factories', FactoryViewSet)
# core_router.register(r'admin-regions', AdminRegionViewSet)
# core_router.register(r'cities', CityViewSet)

# # POSO routes
# # poso_router.register(r'suppliers', SupplierViewSet)
# # poso_router.register(r'customers', CustomerViewSet)
# # poso_router.register(r'purchase-orders', PurchaseOrderViewSet)
# # poso_router.register(r'purchase-order-items', PurchaseOrderItemViewSet)
# # poso_router.register(r'sales-orders', SalesOrderViewSet)
# # poso_router.register(r'sales-order-items', SalesOrderItemViewSet)
# # poso_router.register(r'payments', PaymentViewSet)
# # poso_router.register(r'invoices', InvoiceViewSet)

# # INVENTORY routes
# inventory_router.register(r'warehouses', WarehouseViewSet)
# inventory_router.register(r'product-packages', ProductPackageViewSet)
# inventory_router.register(r'products', ProductViewSet)
# inventory_router.register(r'stocks', StockViewSet)
# inventory_router.register(r'inventory-movements', InventoryMovementViewSet)
# inventory_router.register(r'stock-transfers', StockTransferViewSet, basename='stock-transfer')

# # Users Routes
# users_router.register(r'users', UserViewSet)
# # Sales Order router
# so_router.register(r'salesorders', SalesOrderViewSet, basename='salesorder')
# so_router.register(r'salesorderitems', SalesItemViewSet, basename='salesorderitem')

# # -----------------------------
# # URL Patterns
# # -----------------------------
# urlpatterns = [
#     # Admin panel
#     path('admin/', admin.site.urls),

#     # Authentication (Djoser + JWT)
#     path('auth/', include('djoser.urls')),          # /auth/users/, /auth/users/me/
#     path('auth/', include('djoser.urls.jwt')),      # /auth/jwt/create/, etc.

#     # Custom admin creation
#     path('cd/', CreateAdminUserView.as_view(), name="create-admin"),

#     # API Groups (Prefixed by app)
#     path('core/', include(core_router.urls)),         # e.g. /core/companies/
#     # path('poso/', include(poso_router.urls)),         # e.g. /poso/suppliers/
#     path('so/', include(so_router.urls)),   # e.g. /sales-orders/
#     path('inventory/', include(inventory_router.urls)),  # e.g. /inventory/products/
#     path('users/', include(users_router.urls)),  # e.g. /users/

#     # # API Docs
#     path(
#         'api/schema/',
#         get_schema_view(
#             title="Milki System API",
#             description="Centralized ERP API Schema",
#             version="1.0.0"
#         ),
#         name='openapi-schema'
#     ),
#     # path('api/docs/', include_docs_urls(title="Milki System API Documentation")),
# ]

# # Media handling (development only)
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
# from rest_framework.documentation import include_docs_urls  # Enable if needed

from main.cd import CreateAdminUserView

# -----------------------------
# Import ViewSets
# -----------------------------

# CORE
from apps.core.views import (
    CityViewSet, CompanyViewSet, FactoryViewSet, AdminRegionViewSet
)

# SALES (replacing POSO)
from main.views import FrontendAppView
from apps.sales.views import SalesOrderViewSet, SalesItemViewSet

# INVENTORY
from apps.inventory.views import (
    WarehouseViewSet, ProductPackageViewSet, ProductViewSet,
    StockViewSet, InventoryMovementViewSet, StockTransferViewSet
)

# USERS
from apps.users.views import UserViewSet

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

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

# INVENTORY routes
inventory_router.register(r'warehouses', WarehouseViewSet)
inventory_router.register(r'product-packages', ProductPackageViewSet)
inventory_router.register(r'products', ProductViewSet)
inventory_router.register(r'stocks', StockViewSet)
inventory_router.register(r'inventory-movements', InventoryMovementViewSet)
inventory_router.register(r'stock-transfers', StockTransferViewSet, basename='stock-transfers')

# USERS routes
users_router.register(r'users', UserViewSet)


# -----------------------------
# Admin UI Branding
# -----------------------------
admin.site.site_header = "Milki System Administration"
admin.site.site_title = "Milki Admin Portal"
admin.site.index_title = "Welcome to Milki Management Dashboard"


# -----------------------------
# URL Patterns
# -----------------------------
urlpatterns = [
    # ... other paths (admin, etc.)

    # 1. This view generates the actual schema (YAML/JSON)
    # USE SpectacularAPIView, NOT get_schema_view
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
