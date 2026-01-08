import os
import django
import sys
from pathlib import Path
import json

print("Starting verification script...")

# sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aichatbot.settings')
try:
    django.setup()
    print("Django setup complete.")
except Exception as e:
    print(f"Django setup failed: {e}")
    sys.exit(1)

from organization.models import BotSettings, Organization
from aichatbot.utils import set_organization_slug, clear_organization_slug
from rest_framework.test import APIRequestFactory
from organization.views import ChatWithAgentView
from chat.models import ChatRoom

def verify_chat():
    org_slug = "searchtest"
    set_organization_slug(org_slug)
    
    # Ensure Bot Settings exist
    settings = BotSettings.objects.first()
    if not settings:
        print("Creating default BotSettings for testing...")
        BotSettings.objects.create(
            name="Test Bot",
            domain="General",
            required_attributes={"color": "string"},
            system_prompt="You are a helpful assistant.",
            intent_prompt="Classify query as 'general' or 'product_search'.",
            attribute_extraction_prompt="Extract JSON attributes.",
            product_recommendation_prompt="Recommend products."
        )

    print("\n--- Testing General Query ---")
    factory = APIRequestFactory()
    view = ChatWithAgentView.as_view()
    
    # 1. General Query
    req1 = factory.post('/api/chat/', {"prompt": "Hello via API"}, format='json')
    # Manually adding organization middleware logic simulation or ensuring slug is picked up?
    # The view calls get_organization_slug(). We set it in thread local above. 
    
    resp1 = view(req1)
    
    print(f"Status Code: {resp1.status_code}")
    if resp1.status_code == 200:
        print("Response Stream:")
        try:
            for chunk in resp1.streaming_content:
                print(chunk.decode('utf-8'))
        except Exception as e:
            print(f"Stream error: {e}")

    print("\n--- Testing Product Query ---")
    # 2. Product Query
    req2 = factory.post('/api/chat/', {"prompt": "I want a red dress"}, format='json')
    resp2 = view(req2)
    
    print(f"Status Code: {resp2.status_code}")
    if resp2.status_code == 200:
        print("Response Stream:")
        try:
            for chunk in resp2.streaming_content:
                print(chunk.decode('utf-8'))
        except Exception as e:
            print(f"Stream error: {e}")

    clear_organization_slug()

if __name__ == "__main__":
    verify_chat()
