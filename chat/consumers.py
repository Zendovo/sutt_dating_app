from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from user.models import ChatRequest

import json


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["chat_id"]
        self.room_group_name = "chat_%s" % self.room_name
        self.user = self.scope["user"]

        # TODO
        # Check if user can access this chat

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        sender = text_data_json["sender"]

        # Save message to database
        await self.save_message(message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message",
                                   "message": message, "sender": sender}
        )

    @database_sync_to_async
    def save_message(self, msg):
        profile = self.user.userprofile
        chat_id = int(self.room_group_name.split('chat_')[1])

        chat = ChatRequest.objects.get(id=chat_id)
        chat.chatmessages_set.exclude(sender=profile).update(seen=True)
        chat.chatmessages_set.create(message=msg, sender=profile)
        return

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "sender": sender}))
