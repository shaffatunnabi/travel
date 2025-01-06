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
        print("WebSocket connect attempt")
        await self.accept()
        print("WebSocket connected!")
        await self.send(text_data=json.dumps({
            'answer': 'Hello! How can I help you today?'
        }))

    async def disconnect(self, close_code):
        print(f"WebSocket disconnected with code: {close_code}")

    async def receive(self, text_data):
        print(f"Received message: {text_data}")
        try:
            data = json.loads(text_data)
            question_id = data.get('question_id')
            
            # FAQ database
            faq_responses = {
                '1': {
                    'question': 'What are main advantages of using your service?',
                    'answer': 'Our service offers easy booking, 24/7 customer support, best price guarantees, and personalized travel recommendations.'
                },
                '2': {
                    'question': 'How can I cancel my booking?',
                    'answer': 'You can cancel your booking up to 48 hours before departure through your account dashboard or by contacting our support team.'
                },
                '3': {
                    'question': 'Do you offer group discounts?',
                    'answer': 'Yes! We offer special discounts for groups of 5 or more people. Contact our support team for details.'
                },
                '4': {
                    'question': 'What payment methods do you accept?',
                    'answer': 'We accept all major credit cards, PayPal, and bank transfers. All payments are secured with encryption.'
                },
                '5': {
                    'question': 'How do I contact customer support?',
                    'answer': 'You can reach our support team 24/7 via chat, email at support@jointjourneys.com, or phone at +1-234-567-8900.'
                }
            }

            if question_id in faq_responses:
                response = faq_responses[question_id]
                await self.send(text_data=json.dumps({
                    'question': response['question'],
                    'answer': response['answer']
                }))
            else:
                await self.send(text_data=json.dumps({
                    'error': 'Question not found'
                }))
        except Exception as e:
            print(f"Error: {str(e)}")
            await self.send(text_data=json.dumps({
                'error': str(e)
            })) 