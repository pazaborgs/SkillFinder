from django import forms
from services.models import Service
from accounts.models import ServiceType

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        exclude = ["owner"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price_range': forms.TextInput(attrs={'class': 'form-control'}),
            'service_type': forms.Select(attrs={'class': 'form-control'}),
        }
        

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