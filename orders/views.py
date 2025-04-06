from rest_framework import viewsets
from .permissions import IsOwnerOrAdminOrAssignedDelivery
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsOwnerOrAdminOrAssignedDelivery]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return Order.objects.all()
        elif hasattr(user, 'rol') and user.rol.nombre.lower() == 'delivery':
            return Order.objects.filter(delivery_user=user)
        else:
            return Order.objects.filter(client=user)

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsOwnerOrAdminOrAssignedDelivery]
