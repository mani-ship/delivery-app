from rest_framework import serializers
from .models import DeliveryAgent

class DeliveryAgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAgent
        fields = '__all__'
