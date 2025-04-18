from django.db import models
from django.contrib.auth.models import AbstractUser
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import unicodedata
import re

# Tipos de serviço
class ServiceType(models.Model):
    SERVICE_TYPE_CHOICES = (
        ('electrician', 'Eletricista'),
        ('plumber', 'Encanador'),
        ('painter', 'Pintor'),
        ('cleaner', 'Faxineiro'),
        ('gardener', 'Jardineiro'),
        ('mechanic', 'Mecânico'),
        ('carpenter', 'Carpinteiro'),
        ('nanny', 'Babá'),
        ('tutor', 'Professor Particular'),
        ('tech_support', 'Suporte Técnico'),
    )

    name = models.CharField(max_length=50, choices=SERVICE_TYPE_CHOICES, unique=True)

    def __str__(self):
        return dict(self.SERVICE_TYPE_CHOICES).get(self.name, self.name)

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('user', 'Usuário'),
        ('provider', 'Prestador'),
    )

    # Info
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    phone = models.CharField(max_length=15, blank=True)
    service_types = models.ManyToManyField(ServiceType, blank=True)
    
    # Location
    address = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True)
    
    # Ratings
    average_rating = models.FloatField(default=0.0, blank=True, null=True)
    total_ratings = models.IntegerField(default=0, blank=True, null=True)
    
    def is_provider(self):
        return self.user_type == 'provider'

    def is_user(self):
        return self.user_type == 'user'
    
    def geocode_address(self):
        if self.address and (not self.latitude or not self.longitude):
            geolocator = Nominatim(user_agent= "accounts")
            try:
                location = geolocator.geocode(self.address, timeout=10)
                if location:
                    self.latitude = location.latitude
                    self.longitude = location.longitude
                    self.save()
            except GeocoderTimedOut:
                pass
            
    def clean_city(self):
        '''Remove acentos, espaços e aplica lower()'''
        normalized_city = unicodedata.normalize('NFKD', self.city)
        cleaned_city = re.sub(r'\s+', '', normalized_city).lower()
        return cleaned_city

    def save(self, *args, **kwargs):
        
        if self.city:
            self.city = self.clean_city()
        
        if self.address and (not self.latitude or not self.longitude):
            self.geocode_address()
        super().save(*args, **kwargs)

class Rating(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='ratings')
    score = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # Avaliações de 1 a 5
    created_at = models.DateTimeField(auto_now_add=True)
