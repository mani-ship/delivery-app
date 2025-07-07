from rest_framework import serializers
from .models import DeliveryAgent
from django.contrib.auth.hashers import make_password
class DeliveryAgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAgent
        fields = '__all__'
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    

from rest_framework import serializers
from app.models import OrderAddressMapping, UserAddress

class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ['address']

class OrderAddressMappingSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(source='order.id')
    address = UserAddressSerializer()

    class Meta:
        model = OrderAddressMapping
        fields = ['order_id', 'address']
