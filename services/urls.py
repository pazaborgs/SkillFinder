from django.urls import path
from .views import provider_notification_list, new_service, provider_delete_notification, provider_view_notification, edit_service, user_provider_list, user_view_provider, user_request_service

urlpatterns = [
    path('new_service/', new_service, name='new_service'),
    path('provider_notification_list/', provider_notification_list, name='provider_notification_list'),
    path('provider_delete_notification/<int:id>/', provider_delete_notification, name='provider_delete_notification'),
    path('provider_view_notification/<int:id>/', provider_view_notification, name='provider_view_notification'),
    path('edit_service/<int:id>', edit_service, name = 'edit_service'),
    path('user_provider_list', user_provider_list, name = 'user_provider_list'),
    path('user_view_provider/<int:id>', user_view_provider, name = 'user_view_provider'),
    path('user_request_service', user_request_service, name = 'user_request_service'),

]