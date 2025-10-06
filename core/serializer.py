# core/serializers.py

from rest_framework import serializers
from .models import AdminRegion, City, Company, Factory


# -----------------------------
# AdminRegion Serializer
# -----------------------------
class AdminRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminRegion
        fields = ['id', 'name', 'code', 'description', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


# -----------------------------
# City Serializer
# -----------------------------
class CitySerializer(serializers.ModelSerializer):
    # Nested representation of the admin region
    admin_region = AdminRegionSerializer(read_only=True)
    admin_region_id = serializers.PrimaryKeyRelatedField(
        queryset=AdminRegion.objects.all(),
        source='admin_region',
        write_only=True
    )

    class Meta:
        model = City
        fields = ['id', 'name', 'admin_region', 'admin_region_id', 'description', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


# -----------------------------
# Company Serializer
# -----------------------------
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'description', 'logo_url', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


# -----------------------------
# Factory Serializer
# -----------------------------
class FactorySerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(),
        source='company',
        write_only=True
    )

    city = CitySerializer(read_only=True)
    city_id = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(),
        source='city',
        write_only=True
    )

    admin_region = AdminRegionSerializer(read_only=True)
    admin_region_id = serializers.PrimaryKeyRelatedField(
        queryset=AdminRegion.objects.all(),
        source='admin_region',
        write_only=True
    )

    class Meta:
        model = Factory
        fields = [
            'id', 'name', 'description', 'location', 'unique_location', 'capacity', 'status',
            'company', 'company_id', 'city', 'city_id', 'admin_region', 'admin_region_id',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
