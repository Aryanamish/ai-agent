from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.management import call_command
from django.conf import settings
from .models import Organization, Products
import logging
import json
import os

logger = logging.getLogger(__name__)

# Try to import langchain components, handle if missing for initial setup
try:
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
except ImportError:
    GoogleGenerativeAIEmbeddings = None

@receiver(post_save, sender=Organization)
def create_org_database(sender, instance, created, **kwargs):
    if created and instance.slug:
        slug = instance.slug
        if slug not in settings.DATABASES:
             new_db = settings.DATABASES['default'].copy()
             new_db['NAME'] = settings.BASE_DIR / f"db/{slug}.sqlite3"
             settings.DATABASES[slug] = new_db
        
        try:
            call_command('migrate', database=slug, interactive=False)
        except Exception as e:
            logger.error(f"Failed to migrate database for organization {slug}: {e}")
            print(f"Failed to migrate database for organization {slug}: {e}")


