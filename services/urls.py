from django.urls import path
from .views import my_services, new_service, delete_service, single_service, edit_service

urlpatterns = [
    path('new_service/', new_service, name='new_service'),
    path('my_services/', my_services, name='my_services'),
    path('delete_service/<int:id>/', delete_service, name='delete_service'),
    path('single_service/<int:id>/', single_service, name='single_service'),
    path('edit_service/<int:id>', edit_service, name = 'edit_service')

]