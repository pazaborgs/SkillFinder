from django.db import models
from django.conf import settings

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


class Comment(models.Model):

    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user} on {self.service}'

