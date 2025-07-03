from django.urls import path
from .views import RegisterView,MyTokenObtainPairView,UpdateLocationView, FrequentlyBoughtTogetherView,ForgotPasswordView,ResetPasswordView,CreateOrderView,RandomProductsView,UpdateLocationView,AddressListCreateView,AddressDetailView,CartUpdateQuantityView,get_product_by_id,PlaceOrderView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.urls import path
from .views import (
    CategoryListCreateView,
    CategoryRetrieveUpdateDestroyView,
    ProductListCreateView,
    ProductRetrieveUpdateDestroyView,
)

from django.urls import path
from .views import (
    user_cart,
    CartItemDeleteView,
    CheckoutView,
    OrderListView
)

urlpatterns = [
    #register and login and tiken generating urls
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),    
   

    # Category URLs
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category-detail'),

    # Product URLs
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-detail'),
    path('get-product/<int:pk>/', get_product_by_id, name='get-product-by-id'),


    #cart urls
    path('api/cart/', user_cart),
    path('cart/<int:pk>/delete/', CartItemDeleteView.as_view(), name='cart-delete'),
     path('cart/update-quantity/', CartUpdateQuantityView.as_view(), name='update-cart-quantity'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('orders/', OrderListView.as_view(), name='order-list'),

    #location urls
    path('location/update/', UpdateLocationView.as_view(), name='update-location'),

    #frequent urls
    path('products/<int:product_id>/frequently-bought-together/', FrequentlyBoughtTogetherView.as_view()),

    #password reset urls
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),

    path('create-order/', CreateOrderView.as_view(), name='create-order'),
    path('random-products/', RandomProductsView.as_view(), name='random-products'),

   
    path('user/address/', AddressListCreateView.as_view(), name='user-address'),
    path('user/addresses/<int:pk>/', AddressDetailView.as_view(), name='address-detail'),

    path('place-order/', PlaceOrderView.as_view(), name='place-order'),

]




