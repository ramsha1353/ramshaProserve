from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Address = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=20)
    experiance = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=10)
    user_type = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username