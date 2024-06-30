# notifications/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import *
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async



class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'notifications'
        await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

        await self.accept()

        # Send unviewed notifications
        unviewed_notifications = await self.get_unviewed_notifications()

        for notification in unviewed_notifications:
            order = await self.get_order_from_notifications(notification)
            await self.send(text_data=json.dumps({
                'notification': notification.message,
                'viewed': notification.viewed,
                'order_id': order.pk,
            
            }))
            # await self.mark_as_viewed(notification)
  


    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        print(text_data)
        await self.send(text_data=json.dumps({
            'message': 'Notification received'
        }))

    async def send_notification(self, event):
        print(event['notification'].message)
        await self.send(text_data=json.dumps({
            'notification': event['notification']
        }))

    @sync_to_async
    def get_unviewed_notifications(self):
        notifications = Notification.objects.all()
        return list(notifications)
    
    @sync_to_async
    def get_order_from_notifications(self,notifications):
        return notifications.order

    @database_sync_to_async
    def mark_as_viewed(self, notification):
        notification.viewed = True
        notification.save()
