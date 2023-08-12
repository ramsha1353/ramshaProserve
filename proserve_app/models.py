from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Address = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=20)
    user_type = models.CharField(max_length=20)
    
    def __str__(self):
        return self.user.username




class WorkerProfile(models.Model):
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    service = models.CharField(max_length=100)
    description = models.TextField()
    experiance = models.CharField(max_length=100, blank=True)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    available_time = models.CharField(max_length=100)
    # gender = models.CharField(max_length=10, default='male')
    
