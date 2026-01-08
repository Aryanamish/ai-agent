from django.http import StreamingHttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import BotSettings, Organization
from chat.models import ChatRoom, ChatMessages
from .agent import run_agent
from aichatbot.utils import get_organization_slug
import json

from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser

from .models import Organization, Products, BotSettings
from .serializers import (
    OrganizationSerializer,
    ProductListSerializer,
    ProductsSerializer,
    BotSettingsSerializer,
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAdminUser]

class BotSettingsViewSet(viewsets.ModelViewSet):
    queryset = BotSettings.objects.all()
    serializer_class = BotSettingsSerializer
    permission_classes = [IsAdminUser]

class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer
        return ProductsSerializer

    permission_classes = [IsAdminUser]
    pagination_class = StandardResultsSetPagination


class ChatWithAgentView(APIView):
    def post(self, request, *args, **kwargs):
        # 1. Get Organization Context
        org_slug = get_organization_slug()
        if not org_slug:
            return Response({"error": "Organization context missing."}, status=status.HTTP_400_BAD_REQUEST)
        
        prompt = request.data.get('prompt')
        room_id = request.data.get('room_id')
        
        if not prompt:
            return Response({"error": "Prompt is required."}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Get or Create Room
        if room_id:
            room = get_object_or_404(ChatRoom, id=room_id)
        else:
            room = ChatRoom.objects.create(name=f"Chat {prompt[:20]}")
            
        # 3. Save User Message
        ChatMessages.objects.create(
            room=room,
            sender="user",
            message=prompt
        )
        
        # 4. Get Bot Settings
        # Assuming only one bot setting per org for now? Or get first.
        bot_settings = BotSettings.objects.first() 
        if not bot_settings:
            # Fallback or Error
            return Response({"error": "Bot settings not found for this organization."}, status=status.HTTP_404_NOT_FOUND)
            
        # 5. Fetch Chat History
        # LangChain expects (HumanMessage, AIMessage) format
        history_msgs = ChatMessages.objects.filter(room=room).order_by('timestamp')
        chat_history = []
        from langchain_core.messages import HumanMessage, AIMessage
        for msg in history_msgs:
            if msg.sender == 'user':
                chat_history.append(HumanMessage(content=msg.message))
            else:
                chat_history.append(AIMessage(content=msg.message))

        # 6. Run Agent & Stream
        # Generator function for StreamingHttpResponse
        def event_stream():
            final_response_content = ""
            # Ensure context is active for the generator logic
            from aichatbot.utils import set_organization_slug
            set_organization_slug(org_slug)

            try:
                for event in run_agent(prompt, chat_history, org_slug, bot_settings):
                    # event is a dict of state updates from nodes
                    # we want to extract the final response chunks or status updates
                    
                    # Example event structure from langgraph stream: 
                    # {'node_name': {'key': 'value'}}
                    
                    data_to_send = {}
                    
                    for node_name, state_update in event.items():
                        if 'final_response' in state_update:
                             chunk = state_update['final_response']
                             final_response_content = chunk # In this simple graph it returns full text, not tokens
                             data_to_send = {"type": "answer", "content": chunk}
                        elif 'missing_attributes' in state_update:
                             # We could signal that we are asking a question
                             pass
                        elif 'intent' in state_update:
                             if state_update['intent']:
                                data_to_send = {"type": "status", "content": f"Intent: {state_update['intent']}"}
                        elif 'search_results' in state_update:
                             # Only send status if we actually searched
                             data_to_send = {"type": "status", "content": "Searching products..."}
                    
                    if data_to_send:
                        yield f"data: {json.dumps(data_to_send)}\n\n"
                
                # After loop, save AI response to DB
                if final_response_content:
                    # Re-assert context in case it was lost/cleared
                    set_organization_slug(org_slug)
                    
                    ChatMessages.objects.create(
                        room=room,
                        sender="bot",
                        message=final_response_content
                    )
                    
            except Exception as e:
                yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"

        response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
        response['X-Room-ID'] = str(room.id)
        return response
