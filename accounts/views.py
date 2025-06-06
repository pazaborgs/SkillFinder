from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm, LoginForm
#from django.contrib import messages
from services.models import Notification
from services.forms import ProviderFilterForm
from .models import CustomUser
from django.conf import settings

user = settings.AUTH_USER_MODEL

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            form.save_m2m()  # ManyToMany (service_types)
            return redirect("login")
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()
    
    return render(request, "accounts/register.html", {"form": form})



def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.user_type == "provider":
                    return redirect("provider_interface")
                else:
                    return redirect("user_interface")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


def provider_interface(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(provider=request.user)
    else:
        notifications = []
    return render(request, "services/provider_notification_list.html", {"notifications": notifications})


def user_interface(request):
    if request.user.is_authenticated:
        
        form = ProviderFilterForm(request.GET)
        providers = CustomUser .objects.filter(user_type='provider')
        if form.is_valid():
            name_filter = form.cleaned_data.get('name')
            city_filter = form.cleaned_data.get('city')
            service_type_filter = form.cleaned_data.get('service_type')

            if name_filter:
                providers = providers.filter(username__icontains=name_filter)

            if city_filter:
                providers = providers.filter(city__icontains=city_filter)

            if service_type_filter:
                providers = providers.filter(service_types__name=service_type_filter)

            return render(request, 'services/user_provider_list.html', {'providers': providers, 'form': form})
        
    else:
        providers = []
        return render(request, "services/user_provider_list.html", {"providers": providers})


def homepage(request):
    return render(request, "accounts/homepage.html")
