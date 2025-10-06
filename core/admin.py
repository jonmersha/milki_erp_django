# core/admin.py

from django.contrib import admin
from .models import AdminRegion, City, Company, Factory

# -----------------------------
# AdminRegion Admin
# -----------------------------
@admin.register(AdminRegion)
class AdminRegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'status', 'created_at')
    search_fields = ('name', 'code', 'description')
    list_filter = ('status',)
    readonly_fields = ('id', 'created_at', 'updated_at')


# -----------------------------
# City Admin
# -----------------------------
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'admin_region', 'status', 'created_at')
    search_fields = ('name', 'description', 'admin_region__name')
    list_filter = ('status', 'admin_region')
    readonly_fields = ('id', 'created_at', 'updated_at')


# -----------------------------
# Company Admin
# -----------------------------
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('status',)
    readonly_fields = ('id', 'created_at', 'updated_at')


# -----------------------------
# Factory Admin
# -----------------------------
@admin.register(Factory)
class FactoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'company', 'city', 'admin_region', 'capacity', 'status', 'created_at')
    search_fields = ('name', 'description', 'company__name', 'city__name', 'admin_region__name')
    list_filter = ('status', 'company', 'city', 'admin_region')
    readonly_fields = ('id', 'created_at', 'updated_at')
