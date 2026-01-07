import os
import django
import sys
from pathlib import Path
import time

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aichatbot.settings')
django.setup()

from organization.models import Products
from organization.search import search_products
from aichatbot.utils import set_organization_slug, clear_organization_slug
from django.db import connections

def verify_search():
    org_slug = "searchtest"
    set_organization_slug(org_slug)
    
    print(f"Creating/Migrating '{org_slug}' DB...")
    # Trigger org creation logic manually or just rely on router dynamic creation if we access it?
    # We need to migrate it. 
    # Use migrate_all style logic or just use the management command logic inline.
    from django.conf import settings
    from django.core.management import call_command
    
    if org_slug not in settings.DATABASES:
         new_db = settings.DATABASES['default'].copy()
         new_db['NAME'] = settings.BASE_DIR / f"db/{org_slug}.sqlite3"
         settings.DATABASES[org_slug] = new_db
    
    try:
        call_command('migrate', database=org_slug, interactive=False)
    except Exception as e:
        print(f"Migration warning (might already exist): {e}")

    # Create dummy products
    print("Creating dummy products...")
    p1 = Products.objects.create(
        name="Red Party Dress",
        price=100.00,
        attributes={"color": "red", "occasion": "party", "type": "dress"}
    )
    p2 = Products.objects.create(
        name="Blue Office Shirt",
        price=50.00,
        attributes={"color": "blue", "occasion": "work", "type": "shirt"}
    )
    p3 = Products.objects.create(
        name="Green Casual T-Shirt",
        price=20.00,
        attributes={"color": "green", "occasion": "casual", "type": "t-shirt"}
    )

    print("Checking for embeddings...")
    # Refresh from DB to see if signal updated it
    # Signal might be sync or async? It is sync in Django usually.
    # But it calls an external API, so it might take a second.
    p1.refresh_from_db()
    
    if p1.embedding:
        print("SUCCESS: Embedding generated for Product 1")
    else:
        print("FAILURE: Embedding NOT generated. Check API Key or Signal.")
        # If no embedding, we can't search
        return

    # Test Search
    query = "something for a party"
    print(f"\nSearching for: '{query}'")
    
    # We call the search function (which sets/clears context internally, so we clear ours first to test it properly)
    clear_organization_slug()
    
    results = search_products(query, org_slug, top_k=3)
    
    for r in results:
        print(f" - {r['name']} (Score: {r['score']:.4f})")
    
    if results and results[0]['name'] == "Red Party Dress":
        print("SUCCESS: Search returned correct top result.")
    else:
        print("FAILURE: Search results unexpected.")

if __name__ == "__main__":
    verify_search()
