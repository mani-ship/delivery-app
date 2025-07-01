from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class DeliveryAgent(models.Model):
    id = models.AutoField(primary_key=True)  # NEW auto-incremented ID
    agent_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    mobile_number = models.CharField(max_length=15,)
    whatsapp_number = models.CharField(max_length=15, blank=True)
    address = models.TextField()
    aadhar_card_number = models.CharField(max_length=12,)
    pan_number = models.CharField(max_length=10, )
    driving_license = models.CharField(max_length=20,)
    profile_picture = models.ImageField(upload_to='agent_profiles/', blank=True, null=True)
    password = models.CharField(max_length=128)


    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.name

    @property
    def is_authenticated(self):
        return True
    

    from django.db import models
from django.utils import timezone
import random
import string

class PasswordResetOTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=10)

    def __str__(self):
        return f"{self.email} - {self.otp}"
