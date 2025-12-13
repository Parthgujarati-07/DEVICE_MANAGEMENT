from django.db import models
from django.contrib.auth.models import User

class Device(models.Model):
    DEVICE_TYPES = [
        ('iphone','IPhone'),
        ('android','Android'),
        ('tablet','Tablet'),
    ]

    name = models.CharField(max_length=150)
    device_types = models.CharField(max_length=20,choices=DEVICE_TYPES)
    issued_to = models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,related_name='devices')
    issued_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.device_types})"
    
    