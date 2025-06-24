from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class DeliveryAgentManager(BaseUserManager):
    def create_user(self, agent_id, password=None, **extra_fields):
        if not agent_id:
            raise ValueError("Agent ID is required")
        agent = self.model(agent_id=agent_id, **extra_fields)
        agent.set_password(password)
        agent.save(using=self._db)
        return agent
    
    def create_superuser(self, agent_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(agent_id, password, **extra_fields)

class DeliveryAgent(AbstractBaseUser):
    agent_id = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    mobile_number = models.CharField(max_length=15)
    whatsapp_number = models.CharField(max_length=15)
    address = models.TextField()
    aadhar_card_number = models.CharField(max_length=20)
    pan_number = models.CharField(max_length=20)
    driving_license = models.CharField(max_length=30)
    id_photo = models.ImageField(upload_to='agent/id_photos/')
    profile_picture = models.ImageField(upload_to='agent/profile_pictures/')
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'agent_id'

    objects = DeliveryAgentManager()

    def __str__(self):
        return self.agent_id

  
  

