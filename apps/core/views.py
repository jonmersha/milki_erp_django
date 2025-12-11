# core/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import AdminRegion, City, Company, Factory
from .serializer import AdminRegionSerializer, CitySerializer, CompanySerializer, FactorySerializer


# -----------------------------
# AdminRegion ViewSet
# -----------------------------
class AdminRegionViewSet(viewsets.ModelViewSet):
    queryset = AdminRegion.objects.all().order_by('name')
    serializer_class = AdminRegionSerializer
    permission_classes = [IsAuthenticated]  # Optional: restrict access


# -----------------------------
# City ViewSet
# -----------------------------
class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.select_related('admin_region').all().order_by('name')
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticated]


# -----------------------------
# Company ViewSet
# -----------------------------
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all().order_by('name')
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]


# -----------------------------
# Factory ViewSet
# -----------------------------
class FactoryViewSet(viewsets.ModelViewSet):
    queryset = Factory.objects.select_related('company', 'city', 'admin_region').all().order_by('name')
    serializer_class = FactorySerializer
    permission_classes = [IsAuthenticated]
