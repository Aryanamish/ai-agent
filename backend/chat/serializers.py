from rest_framework import serializers

from .models import ChatMessages, ChatRoom


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['slug', 'name', 'created_at']


class ChatMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessages
        fields = ['sender', 'message', 'timestamp']

