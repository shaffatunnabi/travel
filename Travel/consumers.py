import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Book, Person

# Configure logging
logger = logging.getLogger(__name__)

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

class FAQConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("\n[WebSocket] Connection attempt...")
        await self.accept()
        print("[WebSocket] Connected successfully!")

    async def disconnect(self, close_code):
        print(f"\n[WebSocket] Disconnected with code: {close_code}")

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            question = data.get('question', '')
            
            print("\n" + "="*50)
            print("\n[WebSocket] Question Received:", question)
            print("-"*50)

            # Predefined responses
            faq_responses = {
                'What are your most popular destinations?': 
                    'Our most popular destinations include Paris, Tokyo, New York, Dubai, and Bali.',
                'How can I get the best deals?': 
                    'Book early, check seasonal promotions, and sign up for our newsletter.',
                'Do you have family packages?': 
                    'Yes! We offer comprehensive family packages with kid-friendly activities.',
                'What documents do I need for international travel?': 
                    'Valid passport, necessary visas, and travel insurance documentation.',
            }

            # Get response
            answer = faq_responses.get(question, "I'll help you with that question. Please allow me a moment.")
            
            print("\n[WebSocket] Sending Answer:", answer)
            print("="*50 + "\n")

            # Send response back
            await self.send(text_data=json.dumps({
                'answer': answer
            }))

        except Exception as e:
            print(f"\n[WebSocket] Error: {str(e)}")
            await self.send(text_data=json.dumps({
                'error': str(e)
            })) 