from django.contrib import admin
from django.utils.html import format_html
from .models import AdminRegion, City, Company, Factory

@admin.register(AdminRegion)
class AdminRegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'tracker', 'name', 'status')
    search_fields = ('name', 'tracker')
    list_filter = ('status',)
    ordering = ('name',)
    readonly_fields = ('tracker',)

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'tracker', 'name', 'admin_region', 'status')
    search_fields = ('name', 'tracker', 'admin_region__name')
    list_filter = ('status', 'admin_region')
    ordering = ('name',)
    readonly_fields = ('tracker',)

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'tracker', 'name', 'display_logo', 'city', 'status')
    search_fields = ('name', 'tracker', 'city__name')
    list_filter = ('status', 'city')
    ordering = ('name',)
    readonly_fields = ('tracker', 'logo_preview')

    def display_logo(self, obj):
        """Thumbnail for the list view"""
        if obj.logo:
            return format_html('<img src="{}" style="width: 40px; height: 40px; object-fit: contain;" />', obj.logo.url)
        return "-"
    display_logo.short_description = 'Logo'

    def logo_preview(self, obj):
        """Larger preview for the detail view"""
        if obj.logo:
            return format_html('<img src="{}" style="max-width: 200px; height: auto;" />', obj.logo.url)
        return "No logo uploaded"

@admin.register(Factory)
class FactoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'tracker', 'name', 'company', 'city', 'capacity', 'status')
    search_fields = ('name', 'tracker', 'company__name', 'city__name')
    list_filter = ('status', 'company', 'city')
    ordering = ('name',)
    readonly_fields = ('tracker',)