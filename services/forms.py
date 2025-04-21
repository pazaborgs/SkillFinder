from django import forms
from accounts.models import ServiceType  

class ServiceRequestForm(forms.Form):
    service_type = forms.ModelChoiceField(queryset=ServiceType.objects.all())
    description = forms.CharField(widget=forms.Textarea)
    
class ProviderFilterForm(forms.Form):
    name = forms.CharField(required=False, label='Nome do Provedor')
    city = forms.CharField(required=False, label='Cidade')
    service_type = forms.ChoiceField(
        choices=[('', 'Selecione um Tipo de Serviço')] + list(ServiceType.SERVICE_TYPE_CHOICES),
        required=False,
        label='Tipo de Serviço'
    )