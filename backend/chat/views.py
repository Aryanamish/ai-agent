import json
from datetime import datetime
import logging
from django.contrib.auth import get_user_model
from django.http import StreamingHttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from aichatbot.utils import get_organization_slug
from chat.models import ChatMessages, ChatRoom
from organization.models import BotSettings

from .bot.agent import run_agent
from .serializers import ChatMessagesSerializer, ChatRoomSerializer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

User = get_user_model()

bot = User.objects.filter(username="shopwise_bot").first()


class CreateChatRoomView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        name = request.data.get("name")
        user_id = request.user.id if request.user.is_authenticated else None
        room = ChatRoom.objects.create(name=f'{name[:28]}...', user_id=user_id)
        return Response(
            {"chat_room_id": room.slug},
            status=status.HTTP_201_CREATED,
        )


class ChatWithAgentView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        # 1. Get Organization Context
        org_slug = get_organization_slug()
        if not org_slug:
            return Response(
                {"error": "Organization context missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        message = request.data.get("message")
        if not message:
            return Response(
                {"error": "Prompt is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        prompt = message.get("prompt")
        room_id = request.data.get("chat_room_id")

        if not prompt:
            return Response(
                {"error": "Prompt is required."}, status=status.HTTP_400_BAD_REQUEST
            )
        
        if not room_id:
            return Response(
                {"error": "Chat room ID is required."}, status=status.HTTP_400_BAD_REQUEST
            )


        room = get_object_or_404(ChatRoom, pk=room_id)
        

        # Assuming only one bot setting per org for now? Or get first.
        bot_settings = BotSettings.objects.first()
        if not bot_settings:
            # Fallback or Error
            return Response(
                {"error": "Bot settings not found for this organization."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # LangChain expects (HumanMessage, AIMessage) format
        history_msgs = ChatMessages.objects.filter(room=room).order_by("timestamp")
        chat_history = []
        from langchain_core.messages import AIMessage, HumanMessage

        for msg in history_msgs:
            if msg.sender == self.request.user.id:
                chat_history.append(HumanMessage(content=msg.message.get("prompt")))
            else:
                type = msg.message.get("type")
                if (
                    type == "answer"
                    and len(msg.message.get("content").get("item_suggested")) > 0
                ):
                    # If it's an answer with suggested items, format accordingly
                    content = msg.message.get("content")
                    items = content.get("item_suggested", [])
                    items_cleaned = [{"name": item["name"], "price": item["price"]} for item in items]
                    item_str = json.dumps(items_cleaned)
                    full_content = (
                        f"{content.get('airesponse')}\n\nSuggested Items:\n{item_str}"
                    )
                    chat_history.append(AIMessage(content=full_content))
        ChatMessages.objects.create(
            room=room,
            sender=self.request.user.id,
            message=message,
        )
        # Generator function for StreamingHttpResponse
        def event_stream():
            final_response_content = ""
            # Ensure context is active for the generator logic
            from aichatbot.utils import set_organization_slug

            set_organization_slug(org_slug)
            logger.debug(f"Starting agent run for org: {org_slug}, room: {room.pk}")
            try:
                for event in run_agent(
                    prompt,
                    chat_history,
                    org_slug,
                    bot_settings,
                    room
                ):
                    # event is a dict of state updates from nodes
                    # we want to extract the final response chunks or status updates

                    # Example event structure from langgraph stream:
                    # {'node_name': {'key': 'value'}}

                    data_to_send = {}

                    for node_name, state_update in event.items():
                        if "extracted_attributes" in state_update:
                            current_attrs = room.extracted_attributes or {}
                            current_attrs.update(state_update["extracted_attributes"])
                            room.extracted_attributes = current_attrs
                            room.save()

                        if "final_response" in state_update:
                            resp_data = state_update["final_response"]
                            # resp_data is a dict: {'airesponse': '...', 'item_suggested': [...]}

                            final_response_content = resp_data.get("message")
                            # We can store the full structured response in DB if we want, or just text.
                            # For now, let's store just the text in ChatMessages, or we should switch ChatMessages to JSONField?
                            # Given ChatMessages.message is TextField, we'll store text.
                            # Unless we json dump it. Let's json dump it to be safe or just store text.
                            # User asked for response in format... implying the API response.

                            data_to_send = resp_data.get("message")
                        elif "missing_attributes" in state_update:
                            room.missing_attributes = state_update["missing_attributes"]
                            room.save()
                            # We could signal that we are asking a question
                            pass
                        elif "intent" in state_update:
                            if state_update["intent"]:
                                data_to_send = {
                                    "type": "status",
                                    "content": {
                                        "airesponse": f"Intent: {state_update['intent']}"
                                    },
                                }
                        elif "search_results" in state_update:
                            # Only send status if we actually searched
                            data_to_send = {
                                "type": "status",
                                "content": {"airesponse": "Searching products..."},
                            }

                    if data_to_send:
                        yield f"data: {json.dumps(data_to_send)}\n\n"

                # After loop, save AI response to DB
                if final_response_content:
                    # Re-assert context in case it was lost/cleared
                    set_organization_slug(org_slug)

                    ChatMessages.objects.create(
                        room=room, sender=bot.id, message=final_response_content
                    )

            except Exception as e:
                yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"

        response = StreamingHttpResponse(
            event_stream(), content_type="text/event-stream"
        )
        response["X-Room-ID"] = str(room.pk)
        return response

class UserChatRoomsListView(generics.ListAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatRoom.objects.filter(user_id=self.request.user.id).order_by(
            "-created_at"
        )


class ChatRoomMessagesView(generics.ListAPIView):
    serializer_class = ChatMessagesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        room = get_object_or_404(ChatRoom, slug=slug, user_id=self.request.user.id)
        return ChatMessages.objects.filter(room=room).order_by("timestamp")
