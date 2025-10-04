from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active')
        }),
    ) 

# class TaggedItemInline(GenericStackedInline):
#     autocomplete_fields = ['tag']
#     model = TaggedItem
# class CustomProductAdmin(ProductAdmin):
#         inlines = [TaggedItemInline]  
# admin.site.unregister(Product)
# admin.site.register(Product, CustomProductAdmin)



