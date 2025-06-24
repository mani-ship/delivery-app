from rest_framework import serializers
from .models import DeliveryAgent

class DeliveryAgentSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = DeliveryAgent
        fields = '__all__'  # ✅ Fix: pass '__all__' as a string, not a list

    def create(self, validated_data):
        password = validated_data.pop('password')
        # ✅ Make sure create_user exists in your DeliveryAgent model
        agent = DeliveryAgent.objects.create_user(password=password, **validated_data)
        return agent

