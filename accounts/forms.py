from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser , ServiceType

class CustomUserCreationForm(UserCreationForm):
    service_types = forms.ModelMultipleChoiceField(
        queryset=ServiceType.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'id': 'servicetype-checkbox', 'class': 'form-check-input'}),
        label="Tipos de Serviço (se for prestador)"
    )   
    
    user_type = forms.ChoiceField(
        choices=[
            ('user', 'Usuário'),
            ('provider', 'Prestador'),
        ],
        label="Tipo de Usuário",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    address = forms.CharField(
        max_length=255,
        required=False,
        label="Endereço",
        widget=forms.TextInput(attrs={'id': 'address-input', 'class': 'form-control'})
    )

    class Meta:
        model = CustomUser 
        fields = ('username', 'email', 'phone', 'address', 'city', 'user_type', 'service_types', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')
        service_types = cleaned_data.get('service_types')

        # Prestador precisa escolher pelo menos um tipo de serviço
        if user_type == 'provider' and not service_types:
            self.add_error('service_types', 'Prestadores devem selecionar pelo menos um tipo de serviço.')

        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput())


# ADD RATINGS FORMS