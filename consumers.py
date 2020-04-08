import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import ActiveUser


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
        user_id = data['id']
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'get_user',
                'data': data,
            }
        )
        
    async def get_user(self, event):
        await self.send(text_data=json.dumps(event))