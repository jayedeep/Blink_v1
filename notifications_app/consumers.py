import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']

        self.room_group_name = 'notification_%s' % self.room_name
        print(">>>>>>>>step 444444455555",self.scope['url_route']['kwargs'])

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # message = text_data_json['type']
        print(">>>>>>>comming",text_data)
    #     # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_notification',
                'message': text_data
            }
        )

    # Receive message from room group
    async def send_notification(self, event):
        message = json.loads(event['message'])
        print(">>>>>>>>>>>>>> step 44444444444444")
        # delivery_id=json.loads(event['delivery_id'])
        # Send message to WebSocket
        # new_message={'message':message,'delivery':delivery_id}
        await self.send(text_data=json.dumps(message))