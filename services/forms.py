from django import forms
from services.models import Service

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        exclude = ["owner"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price_range': forms.TextInput(attrs={'class': 'form-control'}),
            'service_type': forms.Select(attrs={'class': 'form-control'}),
        }