# core/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminRegionViewSet, CityViewSet, CompanyViewSet, FactoryViewSet

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'adminregions', AdminRegionViewSet, basename='adminregion')
router.register(r'cities', CityViewSet, basename='city')
router.register(r'companies', CompanyViewSet, basename='company')
router.register(r'factories', FactoryViewSet, basename='factory')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
