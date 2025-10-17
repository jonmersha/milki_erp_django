from django.contrib import admin
from .models import AdminRegion, City, Company, Factory


@admin.register(AdminRegion)
class AdminRegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status')
    search_fields = ('name',)
    list_filter = ('status',)
    ordering = ('name',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'admin_region', 'status')
    search_fields = ('name', 'admin_region__name')
    list_filter = ('status', 'admin_region')
    ordering = ('name',)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','description','logo_url', 'city','status')
    search_fields = ('name',)
    list_filter = ('status',)
    ordering = ('name',)


@admin.register(Factory)
class FactoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'company', 'city', 'capacity', 'status')
    search_fields = ('name', 'company__name', 'city__name')
    list_filter = ('status', 'company', 'city')
    ordering = ('name',)
