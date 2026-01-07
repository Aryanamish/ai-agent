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

@receiver(post_save, sender=Products)
def generate_product_embedding(sender, instance, created, **kwargs):
    # Only generate if embedding is missing or strictly new? 
    # User said "as soon as i create a new product".
    # We can also update it if attributes change, but for now let's stick to created or missing.
    # User said "as soon as i create a new product".
    # We can also update it if attributes change, but for now let's stick to created or missing.
    if created or not instance.embedding:
        try:
            from llm.llm import LLM
            # Initialize LLM with default provider (Ollama as requested)
            llm_instance = LLM(provider="ollama")
            embeddings_model = llm_instance.get_embedding_model()
            
            # Construct text representation
            # Name + Attributes
            text_to_embed = f"{instance.name} "
            if instance.attributes:
                # Flat dump of attributes
                if isinstance(instance.attributes, dict):
                    text_to_embed += " ".join([f"{k}: {v}" for k, v in instance.attributes.items()])
                else:
                    text_to_embed += str(instance.attributes)
            
            vector = embeddings_model.embed_query(text_to_embed)
            
            # We must use .update() to avoid recursion if we called .save() inside post_save
            # But .update() works on QuerySet.
            Products.objects.filter(pk=instance.pk).update(embedding=vector)
            
        except Exception as e:
            logger.error(f"Failed to generate embedding for product {instance.name}: {e}")
            print(f"Failed to generate embedding for product {instance.name}: {e}")
