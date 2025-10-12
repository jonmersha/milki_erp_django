# core/serializers.py

from rest_framework import serializers
from .models import AdminRegion, City, Company, Factory


# -----------------------------
# AdminRegion Serializer
# -----------------------------
class AdminRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminRegion
        fields = ['id', 'name', 'status', 'created_at', 'updated_at']
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
# class FactorySerializer(serializers.ModelSerializer):
#     company = CompanySerializer(read_only=True)
#     company_id = serializers.PrimaryKeyRelatedField(
#         queryset=Company.objects.all(),
#         source='company',
#         write_only=True
#     )

#     city = CitySerializer(read_only=True)
#     city_id = serializers.PrimaryKeyRelatedField(
#         queryset=City.objects.all(),
#         source='city',
#         write_only=True
#     )
#     class Meta:
#         model = Factory
#         fields = [
#             'id', 'name', 'description', 'unique_location', 'capacity', 'status',
#             'company', 'company_id', 'city', 'city_id',
#             'created_at', 'updated_at'
#         ]
#         read_only_fields = ['id', 'created_at', 'updated_at']

from rest_framework import serializers
from .models import Factory


class FactorySerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    city_name = serializers.CharField(source='city.name', read_only=True)

    class Meta:
        model = Factory
        fields = [
            'id',
            'name',
            'description',
            'company',
            'company_name',
            'city',
            'city_name',
            'capacity',
            'status',
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        return Factory.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
# -----------------------------
# ProductPackage Serializer