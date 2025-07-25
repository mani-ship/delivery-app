from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Category, Product,CartItem, Order, OrderItem, Profile
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str

from rest_framework.exceptions import AuthenticationFailed

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate(self, data):
        errors = {}

        if User.objects.filter(username=data['username']).exists():
            errors['username'] = "Username already exists."

        if User.objects.filter(email=data['email']).exists():
            errors['email'] = "Email already exists."

        if errors:
            raise serializers.ValidationError(errors)  # Raise both errors 

        return data

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        try:
            return super().validate(attrs)
        except AuthenticationFailed:
            raise AuthenticationFailed("Invalid username or password")

    

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
    queryset=Category.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price','discount_price','image', 'stock', 'category', 'category_id','country_of_origin', 'shelf_life', 'manufacturer_name', 'manufacturer_address','created_at',]


# serializers.py
from rest_framework import serializers
from .models import Product, CartItem

from rest_framework import serializers
from .models import Product, CartItem

class ProductSerializers(serializers.ModelSerializer):
    quantity_type = serializers.SerializerMethodField()
    quantity_count = serializers.SerializerMethodField()
    in_cart = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'image', 'discount_price', 'in_cart', 'quantity_type', 'quantity_count']

    def get_quantity_type(self, obj):
        user = self.context.get('user')
        if user and user.is_authenticated:
            cart_item = CartItem.objects.filter(user=user, product=obj).first()
            if cart_item:
                return cart_item.quantity_type
        return None

    def get_quantity_count(self, obj):
        user = self.context.get('user')
        if user and user.is_authenticated:
            cart_item = CartItem.objects.filter(user=user, product=obj).first()
            if cart_item:
                return cart_item.quantity_count
        return None

    def get_in_cart(self, obj):
        user = self.context.get('user')
        if user and user.is_authenticated:
            return CartItem.objects.filter(user=user, product=obj).exists()
        return False

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # 🧹 Remove fields with null if not in cart
        if not representation['in_cart']:
            representation.pop('quantity_type', None)
            representation.pop('quantity_count', None)

        # 🖼️ Use relative URL for image
        if instance.image:
            representation['image'] = instance.image.url

        return representation

    



from rest_framework import serializers
from .models import CartItem, Product

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'product_image',
                  'quantity', 'quantity_type', 'quantity_count', 'total_price']

    def get_product_image(self, obj):
        request = self.context.get('request')
        if obj.product.image:
            image_url = obj.product.image.url
            if request is not None:
                return obj.product.image.url 
            return image_url
        return None

    def get_total_price(self, obj):
        return obj.total_price()




class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['product_name','product_image', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'  

    


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['latitude', 'longitude']

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user with this email.")
        return value

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = f"http://localhost:8000/reset-password/{uid}/{token}/"

        print("Password reset link:", reset_link)  

class ResetPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            uid = force_str(urlsafe_base64_decode(data['uid']))
            self.user = User.objects.get(pk=uid)
        except:
            raise serializers.ValidationError("Invalid UID")

        if not default_token_generator.check_token(self.user, data['token']):
            raise serializers.ValidationError("Invalid or expired token")

        return data

    def save(self):
        self.user.set_password(self.validated_data['new_password'])
        self.user.save()



# serializers.py

from rest_framework import serializers
from .models import UserAddress

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = [ 'address', 'phone_number', 'alternate_phone_number','latitude','longitude']


from rest_framework import serializers
from .models import OrderAddressMapping

class OrderItemAddressMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderAddressMapping
        fields = ['order_item', 'address', 'assigned_at']


from rest_framework import serializers
from .models import UserAddress, Order          

class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ['address']

class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['total_amount']
