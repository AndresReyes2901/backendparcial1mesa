from decimal import Decimal
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from .permissions import IsStaffOrSuperUser
from orders.models import Cart


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsStaffOrSuperUser]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.is_staff:
            return Product.objects.all()

        return Product.objects.filter(is_available=True, stock__gt=0)

    @action(detail=True, methods=['post'])
    def apply_discount(self, request, pk=None):
        """Aplica descuento a un solo producto"""
        product = self.get_object()
        try:
            discount_str = str(request.data.get('discount_percentage', '0'))
            discount = float(discount_str)
            if discount < 0 or discount > 100:
                return Response(
                    {"error": "El descuento debe estar entre 0 y 100%"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            product.discount_percentage = Decimal(discount_str)
            product.has_discount = discount > 0
            product.save()

            return Response({
                "message": f"Descuento del {discount}% aplicado correctamente",
                "product": ProductSerializer(product).data
            })
        except (ValueError, TypeError):
            return Response(
                {"error": "Valor de descuento inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'])
    def bulk_discount(self, request):
        """Aplica descuento a múltiples productos"""
        product_ids = request.data.get('product_ids', [])

        if not product_ids:
            return Response(
                {"error": "Debe proporcionar al menos un ID de producto"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            discount_str = str(request.data.get('discount_percentage', '0'))
            discount = float(discount_str)
            if discount < 0 or discount > 100:
                return Response(
                    {"error": "El descuento debe estar entre 0 y 100%"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            products = Product.objects.filter(id__in=product_ids)
            decimal_discount = Decimal(discount_str)
            count = products.update(
                discount_percentage=decimal_discount,
                has_discount=discount > 0
            )
            return Response({
                "message": f"Descuento del {discount}% aplicado a {count} productos"
            })
        except (ValueError, TypeError):
            return Response(
                {"error": "Valor de descuento inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'])
    def recommendations(self, request):
        """Obtiene recomendaciones basadas en el carrito del usuario"""
        user = request.user

        if not user.is_authenticated:
            return Response({"error": "Usuario no autenticado"},
                            status=status.HTTP_401_UNAUTHORIZED)

        try:

            cart = Cart.objects.get(user=user)
            cart_products = [item.product for item in cart.items.all()]

            if not cart_products:

                recommendations = Product.objects.filter(
                    is_active=True,
                    is_available=True
                ).order_by('-id')[:5]
            else:

                recommendations = Product.objects.filter(
                    is_active=True,
                    is_available=True,
                    recommended_for__in=cart_products
                ).exclude(id__in=[p.id for p in cart_products]).distinct()[:5]

            return Response(ProductSerializer(recommendations, many=True).data)

        except Cart.DoesNotExist:

            recommendations = Product.objects.filter(
                is_active=True,
                is_available=True
            ).order_by('-id')[:5]
            return Response(ProductSerializer(recommendations, many=True).data)

