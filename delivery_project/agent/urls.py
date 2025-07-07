from django.urls import path
from .views import DeliveryAgentCreateView,DeliveryAgentLoginView,RequestPasswordResetOTP,VerifyOTPAPIView,ResetPassword,AssignOrderToAgent

urlpatterns = [
    path('register/', DeliveryAgentCreateView.as_view(), name='register-agent'),
    path('login/', DeliveryAgentLoginView.as_view(), name='agent-login'),
    path('request-reset-password/', RequestPasswordResetOTP.as_view(), name='request-reset-password'),
    path('verify-otp/', VerifyOTPAPIView.as_view(), name='verify-otp'),
    path('reset-password/', ResetPassword.as_view(), name='reset-password'),
    path('assign-order/', AssignOrderToAgent.as_view(), name='assign-one-order'),
]
