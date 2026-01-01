from rest_framework import serializers
from .models import AdminRegion, City, Company, Factory

class AdminRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminRegion
        fields = ['tracker', 'name', 'status']
        read_only_fields = ['tracker']

class CitySerializer(serializers.ModelSerializer):
    region_name = serializers.ReadOnlyField(source='admin_region.name')

    class Meta:
        model = City
        fields = ['tracker', 'name', 'admin_region', 'region_name', 'description', 'status']
        read_only_fields = ['tracker']

class CompanySerializer(serializers.ModelSerializer):
    city_name = serializers.ReadOnlyField(source='city.name')
    # Use ImageField to automatically handle absolute URL generation
    logo = serializers.ImageField(required=False, allow_null=True)
    banner = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Company
        fields = [
            'tracker', 'name', 'city', 'city_name', 
            'logo', 'banner', 'description', 'status'
        ]
        read_only_fields = ['tracker']
        

class FactorySerializer(serializers.ModelSerializer):
    company_name = serializers.ReadOnlyField(source='company.name')
    city_name = serializers.ReadOnlyField(source='city.name')

    class Meta:
        model = Factory
        fields = [
            'tracker', 'name', 'company', 'company_name', 
            'city', 'city_name', 'capacity', 'description', 'status'
        ]
        read_only_fields = ['tracker']