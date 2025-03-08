from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants
from django.shortcuts import get_object_or_404, redirect, render
from services.forms import ServiceForm
from django.conf import settings
from .models import Service

user = settings.AUTH_USER_MODEL

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

def my_services(request):

    user = request.user

    name_filter = request.GET.get('name')
    type_filter = request.GET.get('service_type')
    services = Service.objects.filter(owner=user)

    if name_filter:
        services = services.filter(name__icontains = name_filter)

    if type_filter:
        services = services.filter(marketing_niche = type_filter)
    
    types = Service.objects.values_list('service_type', flat=True).distinct()
    
    return render(request, 'services/my_services.html', {'services': services, 'types': types})


def single_service(request, id):
    service = get_object_or_404(Service, id=id)
    return render(request, 'services/single_service.html', {'service': service}) 
    

def delete_service(request, id):
    service = get_object_or_404(Service, id=id)
    service.delete()
    messages.add_message(request, constants.SUCCESS, 'Serviço Excluido')
    return redirect('my_services')

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

# User Views

def user_service_list(request):

    name_filter = request.GET.get('name')
    services = Service.objects.all()

    if name_filter:
        services = services.filter(name__icontains = name_filter)
        
    return render(request, 'services/user_service_list.html', {'services': services})