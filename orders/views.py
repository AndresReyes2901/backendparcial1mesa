import stripe
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from requests import Response
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from SmartCartBackend import settings
from .permissions import IsOwnerOrAdminOrAssignedDelivery,IsCartOwner
from .models import Order, OrderItem, OrderStatusHistory, Cart, CartItem
from .serializers import OrderSerializer, OrderItemSerializer, CartSerializer, CartItemSerializer


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsOwnerOrAdminOrAssignedDelivery]
    filter_backends = [filters.SearchFilter]
    search_fields = ['status', 'client__correo', 'delivery_user__correo']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Order.objects.all()
        elif hasattr(user, 'rol') and user.rol.nombre.lower() == 'delivery':
            return Order.objects.filter(delivery_user=user)
        else:
            return Order.objects.filter(client=user)

    def perform_update(self, serializer):
        old_instance = self.get_object()
        old_status = old_instance.status

        instance = serializer.save()

        if old_status != instance.status:
            OrderStatusHistory.objects.create(
                order=instance,
                status=instance.status,
            )

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)


class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [IsOwnerOrAdminOrAssignedDelivery]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return OrderItem.objects.all()
        elif hasattr(user, 'rol') and user.rol.nombre.lower() == 'delivery':
            return OrderItem.objects.filter(order__delivery_user=user)
        else:
            return OrderItem.objects.filter(order__client=user)


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsOwnerOrAdminOrAssignedDelivery]
    filter_backends = [filters.SearchFilter]
    search_fields = ['client__correo']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Cart.objects.all()
        return Cart.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated,IsCartOwner]

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)



class CheckoutViewSet(APIView):
    permission_classes = [IsAuthenticated,IsCartOwner]

    def post(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, user=request.user)
        line_items = []

        for item in cart.items.all():
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.product.name,
                    },
                    'unit_amount': int(item.product.price * 100),
                },
                'quantity': item.quantity,
            })

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url='http://localhost:8000/payment-success',
            cancel_url='http://localhost:8000/payment-cancel',
            metadata={
                "user_id": request.user.id
            }
        )
        return Response({'checkout_url': session.url})

@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(APIView):
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:

            return Response(status=400)
        except stripe.error.SignatureVerificationError as e:

            return Response(status=400)


        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            user_id = session['metadata']['user_id']


            cart = get_object_or_404(Cart, user_id=user_id)

            order = Order.objects.create(client=cart.user, status="pending")
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                )

            cart.items.all().delete()

        return Response(status=200)