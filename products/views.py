from decimal import Decimal

from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .models import Product
from .serializers import ProductSerializer
from .permissions import IsStaffOrSuperUser
from orders.models import Cart
from django.http import HttpResponse
from datetime import datetime
from .reports import (
    generate_client_report, generate_top_products_report,
    export_to_excel, render_to_pdf
)


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


@login_required
def simple_client_report_view(request):

    client_id = request.GET.get('client_id')
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    if not client_id:
        return HttpResponse("Error: Se requiere un ID de cliente", status=400)

    start_date = None
    end_date = None
    try:
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    except ValueError:
        return HttpResponse("Error: Formato de fecha inválido. Use YYYY-MM-DD", status=400)

    report_data = generate_client_report(client_id, start_date, end_date)


    pdf = render_to_pdf('reports/client_report.html', report_data)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=cliente_{client_id}_reporte.pdf'
        return response
    return HttpResponse("Error generando PDF", status=500)


@login_required
def simple_top_products_report_view(request):

    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    limit = request.GET.get('limit', 10)

    start_date = None
    end_date = None
    try:
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        limit = int(limit)
    except ValueError:
        return HttpResponse("Error: Formato de fecha o límite inválido", status=400)

    report_data = generate_top_products_report(start_date, end_date, limit)


    pdf = render_to_pdf('reports/top_products_report.html', report_data)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=productos_mas_vendidos.pdf'
        return response
    return HttpResponse("Error generando PDF", status=500)