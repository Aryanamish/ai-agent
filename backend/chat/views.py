from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .bot.agent import ChatBot
from .models import ChatRoom


class ChatBotView(APIView):
    def post(self, request):
        message = request.data.get("message")
        room_id = request.data.get("room_id")

        if not message:
            return Response(
                {"error": "Message is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Determine room
        if not room_id:
            # Create a new room if not provided
            room = ChatRoom.objects.create(name=f"Chat {ChatRoom.objects.count() + 1}")
            room_id = room.id
        else:
            # Verify room exists
            if not ChatRoom.objects.filter(id=room_id).exists():
                return Response(
                    {"error": "Invalid room_id"}, status=status.HTTP_404_NOT_FOUND
                )

        try:
            bot = ChatBot()
            response_data = bot.process_message(message, room_id)

            # Add room_id to response so client knows where to continue
            response_data["room_id"] = room_id

            return Response(response_data)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
