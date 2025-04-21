from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants
from django.shortcuts import get_object_or_404, redirect, render
from services.forms import ServiceRequestForm, ProviderFilterForm
from django.conf import settings
from .models import ServiceRequest, Notification, CustomUser
#from geopy.distance import geodesic

user = settings.AUTH_USER_MODEL

# Needs a way to edit profile for both user_type

# === PROVIDER STUFF ===

# Provider Notifications = Provider homepage

@login_required
def provider_notification_list(request):
    user = request.user
    notifications = Notification.objects.filter(provider=user)

    return render(request, 'services/provider_notification_list.html', {'notifications': notifications})

# Open/View - Delete, Notification

def provider_view_notification(request, id):
    notification = get_object_or_404(Notification, id=id)
    notification.is_read = True
    notification.save()
    
    return render(request, 'services/provider_view_notification.html', {'notification': notification}) 

def provider_delete_notification(request, id):
    notification = get_object_or_404(Notification, id= id)
    notification.delete()
    messages.add_message(request, constants.SUCCESS, 'Notificação excluída com sucesso.')
    return redirect('provider_notification_list')

# === USER STUFF ===

# Provider List = User Homepage

def user_provider_list(request):
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

# View Provider Profile

def user_view_provider(request, id):
    provider = get_object_or_404(CustomUser, id=id)
    return render(request, 'services/user_view_provider.html', {'provider': provider})

# Request Service Form

def user_request_service(request):
    if request.method == "POST":
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            service_type = form.cleaned_data['service_type']
            description = form.cleaned_data['description']

            # Criar request
            service_request = ServiceRequest.objects.create(
                requester=request.user,
                service_type=service_type,
                description=description
            )

            #user_coords = (request.user.latitude, request.user.longitude)

            # Filtra provedores por cidade e tipagem correta
            
            providers = CustomUser.objects.filter(
                user_type = 'provider',
                service_types = service_type,
                city = request.user.city,
                #latitude__isnull = False,
                #longitude__isnull = False
            )
            
            for provider in providers:
            #provider_coords = (provider.latitude, provider.longitude)
            #dist_km = geodesic(user_coords, provider_coords).km  
            #if dist_km < 10:
            
                Notification.objects.create(
                    provider = provider,
                    request = service_request,
                    description = service_request.description
                )

            messages.success(request, f"Solicitação para '{service_type}, {description}' enviada com sucesso!")
            return redirect("user_request_service")
    else:
        form = ServiceRequestForm()

    return render(request, "services/user_request_service.html", {"form": form})