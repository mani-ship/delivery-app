from django.db import models

class DeliveryAgent(models.Model):
    agent_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    mobile_number = models.CharField(max_length=15, unique=True)
    whatsapp_number = models.CharField(max_length=15, blank=True)
    address = models.TextField()
    aadhar_card_number = models.CharField(max_length=12, unique=True)
    pan_number = models.CharField(max_length=10, unique=True)
    driving_license = models.CharField(max_length=20, unique=True)
    profile_picture = models.ImageField(upload_to='agent_profiles/', blank=True, null=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.name
