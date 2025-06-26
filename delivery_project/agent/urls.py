from django.urls import path
from .views import AgentRegisterView,AgentLoginView,AgentForgotPasswordView,VerifyAgentOTPView,AgentResetPasswordView

urlpatterns = [
    path('register/', AgentRegisterView.as_view(), name='agent-register'),
    path('login/', AgentLoginView.as_view(), name='agent-login'),
     path('forgot-password/', AgentForgotPasswordView.as_view()),
    path("verify-otp/", VerifyAgentOTPView.as_view()),
    path("set-password/", AgentResetPasswordView.as_view()),
    
]
