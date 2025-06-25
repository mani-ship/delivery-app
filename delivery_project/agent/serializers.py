from rest_framework import serializers
from .models import DeliveryAgent

class DeliveryAgentSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = DeliveryAgent
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password')
        agent = DeliveryAgent.objects.create_user(password=password, **validated_data)
        return agent

from rest_framework import serializers
from .models import DeliveryAgent

class DeliveryAgentLoginSerializer(serializers.Serializer):
    agent_id = serializers.CharField()
    password = serializers.CharField(write_only=True)




from rest_framework import serializers
from django.contrib.auth.models import User

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data
