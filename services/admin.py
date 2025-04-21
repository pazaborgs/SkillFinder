from django.contrib import admin
from .models import ServiceRequest, Notification


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'requester', 'service_type', 'created_at')
    list_filter = ('service_type', 'created_at')
    search_fields = ('requester__username', 'description')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'provider', 'request', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('provider__username', 'request__description')
