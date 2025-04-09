from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer
from .permissions import IsStaffOrSuperUser


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsStaffOrSuperUser]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.is_staff:
            return Product.objects.all()

        return Product.objects.filter(is_available=True, stock__gt=0)
