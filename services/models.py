from django.db import models
from django.conf import settings
from accounts.models import CustomUser, ServiceType

class Service(models.Model):
    SERVICE_TYPE_CHOICES = (
        ('Consultoria', 'Consultoria'),
        ('Manutenção', 'Manutenção'),
        ('Desenvolvimento', 'Desenvolvimento'),
        ('Design', 'Design'),
        ('Outro', 'Outro'),
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100) 
    service_type = models.CharField(max_length=30, choices=SERVICE_TYPE_CHOICES) 
    price_range = models.CharField(max_length=50)


    def __str__(self):
        return self.name
    

class ServiceRequest(models.Model):
    requester = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='requests')
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.requester.username} pediu {self.service_type.name}"


# Notificações internas

class Notification(models.Model):
    provider = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Notificação para {self.provider.username} sobre '{self.request}'"

