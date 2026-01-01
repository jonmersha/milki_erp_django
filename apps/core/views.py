from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import AdminRegion, City, Company, Factory
from .serializers import (
    AdminRegionSerializer, CitySerializer, 
    CompanySerializer, FactorySerializer
)

class AdminRegionViewSet(viewsets.ModelViewSet):
    queryset = AdminRegion.objects.all()
    serializer_class = AdminRegionSerializer
    lookup_field = 'tracker'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all().select_related('admin_region')
    serializer_class = CitySerializer
    lookup_field = 'tracker'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['admin_region', 'status']
    search_fields = ['name']

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all().select_related('city')
    serializer_class = CompanySerializer
    lookup_field = 'tracker'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['city', 'status']
    search_fields = ['name']

class FactoryViewSet(viewsets.ModelViewSet):
    queryset = Factory.objects.all().select_related('company', 'city')
    serializer_class = FactorySerializer
    lookup_field = 'tracker'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['company', 'city', 'status']
    search_fields = ['name']