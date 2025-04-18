from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants
from django.shortcuts import get_object_or_404, redirect, render
from services.forms import ServiceForm, ServiceRequestForm, ProviderFilterForm
from django.conf import settings
from .models import Service, ServiceRequest, Notification, CustomUser
#from geopy.distance import geodesic

user = settings.AUTH_USER_MODEL

# PROVIDER STUFF ===

@login_required
def new_service(request):
    
    if request.method ==  'GET':
        form = ServiceForm()
        return render(request, 'services/new_service.html', {'form': form})

    elif request.method == 'POST':

        form = ServiceForm(request.POST, request.FILES) #
        print(request.user)
        
        if form.is_valid():
            service = form.save(commit=False)
            service.owner = request.user
            service.save()
            messages.add_message(request, constants.SUCCESS, 'Serviço adicionado com sucesso!')
            return redirect('my_services')
       
        else:
            print(form.errors)
            messages.add_message(request, constants.ERROR, 'Serviço não cadastrado')
            return render(request, 'services/new_service.html', {'form': form})

def provider_notification_list(request):
    user = request.user
    notifications = Notification.objects.filter(provider=user)

    return render(request, 'services/provider_notification_list.html', {'notifications': notifications})


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

def edit_service(request, id):
    service = get_object_or_404(Service, id=id)
    form = ServiceForm(request.POST, instance = service) # Bind form to the instance
    
    if request.method == 'POST':
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Success')
            return redirect('single_service', id=service.id)
        else:
            form = ServiceForm(instance=service)
            # add message

    return render(request, 'services/edit_service.html', {'form': form, 'service': service})

# USER VIEWS ===

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

def user_view_provider(request, id):
    provider = get_object_or_404(CustomUser, id=id)
    return render(request, 'services/user_view_provider.html', {'provider': provider})


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