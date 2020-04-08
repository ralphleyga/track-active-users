import json

from django.utils import timezone
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import ActiveUser

USER_STATUS = {
    'offline': 0,
    'active': 1,
    'away': 2
}


class ActiveRoomConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'room_{self.room_name}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()

    async def disconnect(self, code_node):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'get_user',
                'data': data,
            }
        )
        
    async def get_user(self, event):
        data = event['data']
        await self.send(text_data=json.dumps(event))
        await self.update_user(data['id'], data['status'])
    
    @database_sync_to_async
    def update_user(self, user_id, status):
        user = get_user_model().objects.get(id=user_id)
        try:
            active_user = ActiveUser.objects.get(user=user)
            active_user.status = USER_STATUS[status]
            active_user.last_active = timezone.now().date()
            active_user.save()
        except ActiveUser.DoesNotExist:
            active_user, create = ActiveUser.objects.get_or_create(user=user, status=USER_STATUS[status], last_active=timezone.now().date())
        return active_user