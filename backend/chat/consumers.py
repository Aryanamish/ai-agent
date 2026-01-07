import asyncio
import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        # Send a welcome message
        await self.send(text_data=json.dumps({
            "type": "info",
            "content": "Connected to AI Chat Stream. Send a message to see simulated streaming."
        }))

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            user_message = data.get("message", "")
        except json.JSONDecodeError:
            user_message = text_data

        response_text = "Here is a simulated AI response. I am generating this text chunk by chunk to demonstrate streaming capabilities via WebSockets. " * 2
        
        # Simulate streaming
        for i in range(0, len(response_text), 5):
            chunk = response_text[i:i+5]
            await self.send(text_data=json.dumps({
                "type": "stream",
                "content": chunk
            }))
            await asyncio.sleep(0.1)
        
        await self.send(text_data=json.dumps({
            "type": "end",
            "content": ""
        }))
