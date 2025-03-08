from django.urls import path
from .views import (
    register,
    login_view,
    logout_view,
    provider_interface,
    user_interface,
    homepage,
)

urlpatterns = [
    path("", homepage, name="homepage"),
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("provider_interface/", provider_interface, name="provider_interface"),
    path("user/", user_interface, name="user_interface"),
]
