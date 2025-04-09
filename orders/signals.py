from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Order, OrderStatusHistory

@receiver(pre_save, sender=Order)
def track_order_status_change(sender, instance, **kwargs):
    if instance.pk:
        previous = Order.objects.get(pk=instance.pk)
        if previous.status != instance.status:
            OrderStatusHistory.objects.create(
                order=instance,
                previous_status=previous.status,
                new_status=instance.status
            )
