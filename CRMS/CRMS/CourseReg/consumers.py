from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, Group
import json
from channels.db import database_sync_to_async


class GroupChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_id = self.scope['url_route']['kwargs']['group_id']
        self.group = await self.get_group()

        # Join the group's channel group
        await self.channel_layer.group_add(
            self.group_channel_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the group's channel group
        await self.channel_layer.group_discard(
            self.group_channel_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender_id = data['sender_id']
        sender_name =data['sender_name']

        # Create a new message and save it to the group
        await self.create_message_async(self.group, sender_id, message)

        # Broadcast the message to all users in the group
        await self.channel_layer.group_send(
            self.group_channel_name,
            {
                'type': 'group_message',
                'sender_id': sender_id,
                'message': message,
                'sender_name': sender_name
            }
        )

    async def group_message(self, event):
        sender_id = event['sender_id']
        message = event['message']
        sender_name = event['sender_name']
        # Send the message to the WebSocket
        await self.send(text_data=json.dumps({
            'sender_name': sender_name,
            'sender_id': sender_id,
            'message': message,
            'timestamp': self.timestamp if self.timestamp else '-',
            'message_id': self.message_id,
        
        }))

    @database_sync_to_async
    def get_group(self):
        # Retrieve the group based on the provided group_id
        group = Group.objects.get(id=self.group_id)
        return group

    @database_sync_to_async
    def create_message(self, group, sender_id, content):
        if content:
            return Message.objects.create(group=group, sender_id=sender_id, content=content)

    async def create_message_async(self, group, sender_id, message):
        created_message = await self.create_message(group, sender_id, message)
        self.timestamp = str(created_message.timestamp)
        self.message_id = created_message.id

    @property
    def group_channel_name(self):
        return f"group_{self.group_id}"
