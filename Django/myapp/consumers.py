from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.group_name = f'chat_{self.chat_id}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        if 'message' in data:
            message = data['message']
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                }
            )
        elif 'message_id' in data and 'is_read' in data:
            message_id = data['message_id']
            is_read = data['is_read']

            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'update_message_status',
                    'message_id': message_id,
                    'is_read': is_read,
                }
            )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message,
        }))

    async def update_message_status(self, event):
        message_id = event['message_id']
        is_read = event['is_read']

        await self.send(text_data=json.dumps({
            'message_id': message_id,
            'is_read': is_read,
        }))