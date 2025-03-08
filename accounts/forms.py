from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser  
        fields = ('username', 'email', 'user_type') 
        widgets = {
            'password1': forms.PasswordInput(),  
            'password2': forms.PasswordInput(),
        }

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)