from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .models import DeliveryAgent
from .serializers import DeliveryAgentSerializer

class DeliveryAgentCreateView(generics.CreateAPIView):
    queryset = DeliveryAgent.objects.all()
    serializer_class = DeliveryAgentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({
                "message": "Registered successfully"
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "message": "Registration failed",
            "message": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)



from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from agent.models import DeliveryAgent
from rest_framework_simplejwt.tokens import RefreshToken


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import DeliveryAgent
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken

class DeliveryAgentLoginView(APIView):
    def post(self, request):
        agent_id = request.data.get('agent_id')
        password = request.data.get('password')

        try:
            agent = DeliveryAgent.objects.get(agent_id=agent_id)
        except DeliveryAgent.DoesNotExist:
            return Response({'message': 'Invalid agent ID'}, status=status.HTTP_404_NOT_FOUND)

        if not check_password(password, agent.password):
            return Response({'message': 'Incorrect password'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(agent)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PasswordResetOTP
from .utils import generate_otp, send_otp_email
from agent.models import DeliveryAgent  # or your custom user model

class RequestPasswordResetOTP(APIView):
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = DeliveryAgent.objects.get(email=email)
        except DeliveryAgent.DoesNotExist:
            return Response({"error": "Email not found"}, status=status.HTTP_404_NOT_FOUND)

        # delete old OTPs
        PasswordResetOTP.objects.filter(email=email).delete()

        # generate and send OTP
        otp = generate_otp()
        PasswordResetOTP.objects.create(email=email, otp=otp)
        send_otp_email(email, otp)

        return Response({"message": "OTP sent to email"}, status=status.HTTP_200_OK)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PasswordResetOTP
from agent.models import DeliveryAgent

class VerifyOTPAPIView(APIView):
    def post(self, request):
        otp = request.data.get("otp")

        if not otp:
            return Response({"error": "OTP is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            otp_entry = PasswordResetOTP.objects.get(otp=otp)
        except PasswordResetOTP.DoesNotExist:
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

        if otp_entry.is_expired():
            otp_entry.delete()
            return Response({"error": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Store email in session for use in reset password
        request.session["reset_email"] = otp_entry.email

        return Response({"message": "OTP verified successfully"}, status=status.HTTP_200_OK)


from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from agent.models import DeliveryAgent

class ResetPassword(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        confirm_password = request.data.get("confirm_password")

        if not email or not password or not confirm_password:
            return Response({"message": "Email, password and confirm password are required"}, status=400)

        if password != confirm_password:
            return Response({"message": "Passwords do not match"}, status=400)

        try:
            user = DeliveryAgent.objects.get(email=email)
            user.password = make_password(password)
            user.save()
            return Response({"message": "Password reset successful"}, status=200)
        except DeliveryAgent.DoesNotExist:
            return Response({"message": "User not found"}, status=404)



# agent/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from app.models import OrderAddressMapping
from .serializers import OrderAddressMappingSerializer
from agent.models import DeliveryAgent

from agent.models import DeliveryAgent
from app.models import OrderAddressMapping

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from agent.models import DeliveryAgent
from app.models import OrderAddressMapping

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from agent.models import DeliveryAgent
from app.models import OrderAddressMapping

class AssignOrderToAgent(APIView):
    def get(self, request):
        agent_id = request.query_params.get("agent_id")
        if not agent_id:
            return Response({"message": "agent_id is required"}, status=400)

        try:
            agent = DeliveryAgent.objects.get(agent_id=agent_id)
        except DeliveryAgent.DoesNotExist:
            return Response({"message": "Agent not found"}, status=404)

        # Check if agent already has an assigned order
        existing = OrderAddressMapping.objects.filter(assigned_agent=agent).first()
        if existing:
            return Response({
                "order_id": existing.order.id,
                "address": {
                    "flat_no": existing.address.flat_no,
                    "landmark": existing.address.landmark,
                    "street": existing.address.street,
                    "city": existing.address.city,
                    "pincode": existing.address.pincode
                }
            }, status=200)

        # Get the first unassigned order
        unassigned_order = OrderAddressMapping.objects.filter(assigned_agent__isnull=True).first()

        if unassigned_order:
            unassigned_order.assigned_agent = agent
            unassigned_order.save()

            return Response({
                "message": "Order assigned successfully",
                "order_id": unassigned_order.order.id,
               "address": {
                   "flat_no": unassigned_order.address.flat_no,
                   "landmark": unassigned_order.address.landmark,
                    "street": unassigned_order.address.street,
                    "city": unassigned_order.address.city,
                    "pincode": unassigned_order.address.pincode
                }
            }, status=200)

        return Response({"message": "No unassigned orders available"}, status=200)


 