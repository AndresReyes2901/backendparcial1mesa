from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from users.views import RolViewSet, UsuarioViewSet
from products.views import ProductViewSet
from orders.views import OrderViewSet, OrderItemViewSet
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register(r'roles', RolViewSet)
router.register(r'users', UsuarioViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
