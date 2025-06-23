from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView 
from .serializers import MyTokenObtainPairSerializer

from rest_framework import generics, permissions
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer ,ProductSerializers

import razorpay
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from rest_framework import generics, status
from .models import CartItem, Order, OrderItem
from app.models import Product
from .serializers import CartItemSerializer, OrderSerializer

import random

from .utils import get_frequently_bought_together
from .models import Profile, Store
from geopy.distance import geodesic


class RegisterView(APIView):
    def post(self, request):
        ...
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Registration successful."}, status=status.HTTP_201_CREATED)
        # Return only the first error as message
        error_message = list(serializer.errors.values())[0][0]
        return Response({"message": error_message}, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenObtainPairView):
   serializer_class = MyTokenObtainPairSerializer

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Product.objects.all().order_by('-created_at')
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(category__id=category_id)
        return queryset

class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
     def get_queryset(self):
        queryset = Product.objects.all().order_by('-created_at')
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(category__id=category_id)
        return queryset

     def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if not queryset.exists():
            return Response({"message": "No products found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError  # ✅ Import here

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CartItem, Product
from .serializers import CartItemSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import CartItem, Product
from .serializers import CartItemSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import CartItem, Product
from .serializers import CartItemSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_cart(request):
    user = request.user

    if request.method == 'POST':
        product_id = request.data.get('product')
        quantity = request.data.get('quantity', 1)
        quantity_type = request.data.get('quantity_type', '1kg')
        quantity_count = request.data.get('quantity_count', 1)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)

        cart_item, created = CartItem.objects.get_or_create(
            user=user,
            product=product,
            defaults={
                'quantity': quantity,
                'quantity_type': quantity_type,
                'quantity_count': quantity_count
            }
        )
        if not created:
            cart_item.quantity_count += int(quantity_count)
            cart_item.save()

        serializer = CartItemSerializer(cart_item, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'GET':
        items = CartItem.objects.filter(user=user)
        serializer = CartItemSerializer(items, many=True, context={'request': request})
        return Response(serializer.data)




    

class CartItemDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            item = CartItem.objects.get(pk=pk, user=request.user)
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({'message':'Item not found'}, status=404)

class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        cart_items = CartItem.objects.filter(user=user)
        if not cart_items:
            return Response({'message': 'Cart is empty'}, status=400)

        total = sum(item.product.price * item.quantity for item in cart_items)

        order = Order.objects.create(user=user, total_amount=total)
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        cart_items.delete()

        return Response({'message': 'Order placed successfully', 'order_id': order.id})

class OrderHistoryView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')


class UpdateLocationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        lat = request.data.get("latitude")
        lon = request.data.get("longitude")

        if not lat or not lon:
            return Response({"message": "Latitude and longitude are required."}, status=400)

        # Save user location
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile.latitude = lat
        profile.longitude = lon
        profile.save()

        # Check for nearby stores
        user_location = (float(lat), float(lon))
        nearby_stores = []
        for store in Store.objects.all():
            store_location = (store.latitude, store.longitude)
            distance = geodesic(user_location, store_location).km
            if distance <= 5:  # 5 km range
                nearby_stores.append({
                    "name": store.name,
                    "address": store.address,
                    "distance_km": round(distance, 2)
                })

        # If no stores found
        if not nearby_stores:
            return Response({
                "message": "Stores not available in this location."
            }, status=200)

        # If stores found
        return Response({
            "message": "Location updated successfully.",
            
        })


class FrequentlyBoughtTogetherView(APIView):
    def get(self, request, product_id):
        products = get_frequently_bought_together(product_id)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

from .serializers import ForgotPasswordSerializer, ResetPasswordSerializer

class ForgotPasswordView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Password reset link sent (check console)'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Password reset successful'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = request.data.get('amount')  # amount in rupees
        if not amount:
            return Response({"message": "Amount is required"}, status=status.HTTP_400_BAD_REQUEST)

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        payment = client.order.create({
            "amount": int(amount) ,  # convert to paise
            "currency": "INR",
            "payment_capture": 1
        })

        return Response({
            "order_id": payment["id"],
            "amount": payment["amount"],
            "currency": payment["currency"],
            "key": settings.RAZORPAY_KEY_ID
        })

# views.py
import random
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializers

class RandomProductsView(APIView):
    def get(self, request):
        products = Product.objects.all()
        random_products = random.sample(list(products), min(5, len(products)))
        serializer = ProductSerializers(products, many=True)
        return Response(serializer.data)

    


# views.py

from rest_framework import generics, permissions
from .models import UserAddress
from .serializers import AddressSerializer

class AddressListCreateView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)

