from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import DeliveryAgentSerializer
from django.contrib.auth.hashers import make_password

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class AgentRegisterView(APIView):
    def post(self, request):
        serializer = DeliveryAgentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Agent registered successfully'}, status=status.HTTP_201_CREATED)
        
        # Format errors as message string
        error_messages = []
        for field, errors in serializer.errors.items():
            for error in errors:
                error_messages.append(f"{field}: {error}")

        return Response({'message': ' | '.join(error_messages)}, status=status.HTTP_400_BAD_REQUEST)



from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import DeliveryAgent

from django.contrib.auth.hashers import check_password
from .models import DeliveryAgent

class AgentLoginView(APIView):
    def post(self, request):
        agent_id = request.data.get('agent_id')
        password = request.data.get('password')

        agent = DeliveryAgent.objects.filter(agent_id=agent_id).first()
        if not agent:
            return Response({'message': 'Agent not found'}, status=404)

        if not check_password(password, agent.password):  # ← use instance field
            return Response({'message': 'Incorrect password'}, status=400)

        return Response({'message': 'Login successful'}, status=200)





from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.hashers import make_password
from .models import DeliveryAgent, PasswordResetOTP

class AgentForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get("email")

        try:
            agent = DeliveryAgent.objects.get(email_id=email)
        except DeliveryAgent.DoesNotExist:
            return Response({"message": "Agent not found"}, status=status.HTTP_404_NOT_FOUND)

        otp_instance, _ = PasswordResetOTP.objects.get_or_create(agent=agent)
        otp_instance.generate_otp()

        # Send OTP via email
        send_mail(
            subject="Your OTP for Password Reset",
            message=f"Your OTP is {otp_instance.otp}",
            from_email="your_email@gmail.com",  # Replace with your sender email
            recipient_list=[agent.email_id],
            fail_silently=False,
        )

        return Response({"message": "OTP sent to email"}, status=status.HTTP_200_OK)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from .models import DeliveryAgent, PasswordResetOTP

class VerifyAgentOTPView(APIView):
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        try:
            agent = DeliveryAgent.objects.get(email_id=email)
        except DeliveryAgent.DoesNotExist:
            return Response({"message": "Agent not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            otp_instance = PasswordResetOTP.objects.filter(agent=agent, otp=otp).latest('created_at')
        except PasswordResetOTP.DoesNotExist:
            return Response({"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

        if timezone.now() - otp_instance.created_at > timedelta(minutes=5):
            return Response({"message": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST)

        otp_instance.is_verified = True
        otp_instance.save()

        return Response({"message": "OTP verified successfully"}, status=status.HTTP_200_OK)



class SetNewPasswordView(APIView):
    def post(self, request):
        email = request.data.get("email")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if new_password != confirm_password:
            return Response({"message": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            agent = DeliveryAgent.objects.get(email_id=email)
        except DeliveryAgent.DoesNotExist:
            return Response({"message": "Agent not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            otp_instance = PasswordResetOTP.objects.filter(agent=agent, is_verified=True).latest('created_at')
        except PasswordResetOTP.DoesNotExist:
            return Response({"message": "OTP not verified"}, status=status.HTTP_400_BAD_REQUEST)

        agent.password = make_password(new_password)
        agent.save()

        # Clean up
        otp_instance.delete()

        return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)




