from django.db import models
from django.utils import timezone
from datetime import timedelta
from paiment.models  import Order
# Create your models here.

class Notification(models.Model):
    message = models.TextField()
    order = models.ForeignKey(Order,on_delete=models.DO_NOTHING,null=True, blank=True)
    viewed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

    @staticmethod
    def delete_old_notifications(days=7):
        threshold_date = timezone.now() - timedelta(days=days)
        Notification.objects.filter(timestamp__lt=threshold_date).delete()
