from rest_framework import generics
from .models import DeliveryAgent
from .serializers import DeliveryAgentSerializer

class DeliveryAgentCreateView(generics.CreateAPIView):
    queryset = DeliveryAgent.objects.all()
    serializer_class = DeliveryAgentSerializer

