# payments/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Order
from notifications.models import Notification

@receiver(post_save, sender=Order)
def notify_user_on_payment(sender, instance, created, **kwargs):
    if created:
        notification = Notification.objects.create(
            message=f'هناك طلب جديد من طرف الزبون {instance.customer}',
            order=instance
        )
        channel_layer = get_channel_layer()
        group_name = "notifications"
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'send_notification',
                'notification': notification
            }
        )
