from django.urls import path
from .views import DeliveryAgentCreateView

urlpatterns = [
    path('register/', DeliveryAgentCreateView.as_view(), name='register-agent'),
]
