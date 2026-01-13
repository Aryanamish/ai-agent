from django.urls import path

from .views import (
    ChatRoomMessagesView,
    ChatWithAgentView,
    CreateChatRoomView,
    UserChatRoomsListView,
)

urlpatterns = [
    path("", ChatWithAgentView.as_view(), name="chat-agent"),
    path("create/", CreateChatRoomView.as_view(), name="chat-room-create"),
    path("history/", UserChatRoomsListView.as_view(), name="chat-history"),
    path(
        "history/<slug:slug>/",
        ChatRoomMessagesView.as_view(),
        name="chat-room-messages",
    ),
]
