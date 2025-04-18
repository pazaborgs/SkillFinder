from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, ServiceType

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Informações Adicionais", {
            "fields": ("user_type", "phone", "address", "latitude", "longitude", "service_types", "city")
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Informações Adicionais", {
            "fields": ("user_type", "phone", "address", "latitude", "longitude", "service_types", "city")
        }),
    )
    list_display = ("username", "email", "user_type", "is_staff")
    list_filter = ("user_type",)

admin.site.register(ServiceType)