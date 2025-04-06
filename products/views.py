from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer
from .permissions import IsSuperUser, IsStaffOrSuperUser

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsStaffOrSuperUser]
