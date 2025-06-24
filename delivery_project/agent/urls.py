from django.urls import path
from .views import AgentRegisterView, AgentLoginView

urlpatterns = [
    path('register/', AgentRegisterView.as_view(), name='agent-register'),
    path('login/', AgentLoginView.as_view(), name='agent-login'),
]
