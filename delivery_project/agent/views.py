from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import DeliveryAgent
from .serializers import DeliveryAgentSerializer
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken


    
class AgentRegisterView(APIView):
    def post(self, request):
        serializer = DeliveryAgentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Agent registered successfully'}, status=status.HTTP_201_CREATED)
        else:
            print("Validation Errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AgentLoginView(APIView):
    def post(self, request):
        agent_id = request.data.get('agent_id')
        password = request.data.get('password')

        try:
            agent = DeliveryAgent.objects.get(agent_id=agent_id)
        except DeliveryAgent.DoesNotExist:
            return Response({'message': 'Invalid Agent ID'}, status=401)

        if not check_password(password, agent.password):
            return Response({'message': 'Incorrect password'}, status=401)

        refresh = RefreshToken.for_user(agent)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)
