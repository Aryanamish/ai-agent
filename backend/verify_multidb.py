import os
import django
import sys
from pathlib import Path
# Setup Django environment
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aichatbot.settings')
django.setup()
from django.conf import settings
from django.db import connections
from organization.models import Products
from aichatbot.utils import set_organization_slug, clear_organization_slug
def test_strict_routing():
    print("Testing Strict Routing (No Context)...")
    clear_organization_slug()
    try:
        # This should fail because Products has DB_TYPE='org' and no slug is set
        Products.objects.create(name="Fail Product", price=10.00, attributes={})
        print("FAILED: strict routing did not raise exception")
    except Exception as e:
        if "without an active organization context" in str(e):
            print("SUCCESS: strict routing raised expected exception")
        else:
            print(f"FAILED: raised unexpected exception: {e}")
def test_org_routing():
    print("\nTesting Org Routing (With Context)...")
    slug = "testorg"
    set_organization_slug(slug)
    
    # Ensure DB is configured (simulating middleware/router dynamic add)
    # The router logic I wrote handles adding it to settings.DATABASES if missing
    # BUT we need to make sure the sqlite file exists/migrated for it to really work?
    # Or at least that Django tries to use it.
    
    # Let's try to create.
    try:
        # We need to manually migrate this 'testorg' db first for the table to exist?
        # Since we are using sqlite, we can just let it fail on "no such table" 
        # which proves it TRIED to use the new DB.
        # If it uses 'default', it might work (if default has the table).
        # Wait, 'default' DB *should* have the tables if we ran migrate?
        # No, 'default' DB should NOT have 'Products' table in a pure multi-tenant setup?
        # Actually, standard django migrate migrates 'default'.
        # So 'default' probably HAS the table.
        # So we need to prove it uses 'testorg'.
        
        # Checking connection alias
        from aichatbot.db_router import OrganizationRouter
        router = OrganizationRouter()
        db_alias = router.db_for_write(Products)
        print(f"Router returned alias: {db_alias}")
        
        if db_alias == slug:
            print("SUCCESS: Router returned correct alias")
        else:
            print(f"FAILED: Router returned {db_alias} instead of {slug}")
    except Exception as e:
        print(f"Error during org routing test: {e}")
    finally:
        clear_organization_slug()
if __name__ == "__main__":
    test_strict_routing()
    test_org_routing()