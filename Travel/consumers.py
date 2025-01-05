import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Book, Person

class BookingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join a common booking group
        await self.channel_layer.group_add(
            "booking_updates",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the group
        await self.channel_layer.group_discard(
            "booking_updates",
            self.channel_name
        )

    async def receive(self, text_data):
        # Handle received messages from WebSocket
        data = json.loads(text_data)
        message_type = data.get('type')
        
        if message_type == 'booking_request':
            # Process booking
            booking_data = data.get('booking_data')
            booking = await self.save_booking(booking_data)
            
            # Broadcast the booking update
            await self.channel_layer.group_send(
                "booking_updates",
                {
                    "type": "booking_update",
                    "message": {
                        "status": "confirmed",
                        "booking_id": booking.id,
                        "message": f"New booking confirmed for {booking.name}"
                    }
                }
            )

    async def booking_update(self, event):
        # Send booking update to WebSocket
        await self.send(text_data=json.dumps(event["message"]))

    @database_sync_to_async
    def save_booking(self, booking_data):
        return Book.objects.create(**booking_data) 