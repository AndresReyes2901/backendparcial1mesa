from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from users.views import RolViewSet, UsuarioViewSet, CustomPasswordResetView, LogoutView, PasswordResetConfirmView, \
    RegisterClienteView, RegisterDeliveryView
from products.views import ProductViewSet
from orders.views import OrderViewSet, OrderItemViewSet, CartViewSet, CartItemViewSet, CheckoutView, StripeWebhookView
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth import views as auth_views

router = routers.DefaultRouter()
router.register(r'roles', RolViewSet)
router.register(r'users', UsuarioViewSet)
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order-items', OrderItemViewSet, basename='orderitem')
router.register(r'cart', CartViewSet, basename="cart")
router.register(r'cart-items', CartItemViewSet, basename="cart-items")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/logout/', LogoutView.as_view(), name='api_logout'),
    path('api/register-cliente/', RegisterClienteView.as_view(), name='register_cliente'),
    path('api/register-delivery/', RegisterDeliveryView.as_view(), name='register_delivery'),
    path('api/password-reset/', CustomPasswordResetView.as_view(), name='custom_password_reset'),
    path('api/reset-password-confirm/<uid>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('api/checkout/', CheckoutView.as_view(), name='checkout'),
    path('api/stripe/webhook/', StripeWebhookView.as_view(), name='stripe-webhook'),
]
