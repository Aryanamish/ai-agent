from time import sleep
from django.core.management.base import BaseCommand
from django.conf import settings
from organization.models import Products
from llm.llm import LLM
from aichatbot.utils import set_organization_slug, clear_organization_slug
import sys

class Command(BaseCommand):
    help = 'Generate embeddings for products in a specific organization.'

    def add_arguments(self, parser):
        parser.add_argument('org_slug', type=str, help='The slug of the organization to process.')
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force regeneration of embeddings for all products, even if they already exist.',
        )
        parser.add_argument(
            '--timeout',
            action='store_true',
            help='Add timeout between every embeding default 0.',
            default=0,
        )

    def handle(self, *args, **options):
        org_slug = options['org_slug']
        force = options['force']
        timeout = options['timeout']

        self.stdout.write(f"Processing organization: {org_slug}")

        # Set organization context to route to the correct DB
        set_organization_slug(org_slug)

        # Ensure DB connection exists (dynamic add if needed)
        if org_slug not in settings.DATABASES:
             new_db = settings.DATABASES['default'].copy()
             new_db['NAME'] = settings.BASE_DIR / f"db/{org_slug}.sqlite3"
             settings.DATABASES[org_slug] = new_db

        try:
            # Initialize LLM
            try:
                embedding_model = LLM.get_embedding_model()
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Failed to initialize LLM: {e}"))
                return

            if force:
                products = Products.objects.all()
                self.stdout.write(f"Force mode: Processing all {products.count()} products.")
            else:
                products = Products.objects.filter(embedding__isnull=True)
                count = products.count()
                if count == 0:
                    self.stdout.write("No products found needing embeddings.")
                    return
                self.stdout.write(f"Processing {count} products (skipping existing).")

            for product in products:
                try:
                    self.stdout.write(f"Generating embedding for: {product.name}", ending='... ')
                    
                    # Construct text to embed
                    text_to_embed = f"{product.name} "
                    if product.attributes:
                        if isinstance(product.attributes, dict):
                            text_to_embed += " ".join([f"{k}: {v}" for k, v in product.attributes.items()])
                        else:
                            text_to_embed += str(product.attributes)
                    
                    # Generate embedding
                    vector = embedding_model.embed_query(text_to_embed)
                    if timeout > 0:
                        sleep(timeout)
                    
                    # Save (using update to be fast and safe, though iterator is already hitting DB)
                    # For bulk updates we could use bulk_update but loop is safer for error handling per item
                    product.embedding = vector
                    product.save(update_fields=['embedding'])
                    
                    self.stdout.write(self.style.SUCCESS("OK"))
                    
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f"FAILED: {e}"))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error accessing database or processing: {e}"))
        finally:
            clear_organization_slug()
