import uuid

from django.db import models


def generate_chat_slug():
    while True:
        slug = str(uuid.uuid4())
        if not ChatRoom.objects.filter(slug=slug).exists():
            return slug


# Create your models here.
class ChatRoom(models.Model):
    DB_TYPE = 'org'
    slug = models.SlugField(
        primary_key=True, default=generate_chat_slug, editable=False
    )
    name = models.CharField(max_length=255)
    user_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class ChatMessages(models.Model):
    DB_TYPE = 'org'
    room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    message = models.JSONField(default=dict)
    sender = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.message[:20]}..."