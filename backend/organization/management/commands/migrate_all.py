from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from organization.models import Organization
class Command(BaseCommand):
    help = 'Migrates all organization databases and the default database'
    def handle(self, *args, **options):
        # 1. Migrate default database
        self.stdout.write("Migrating 'default' database...")
        call_command('migrate', database='default')
        self.stdout.write(self.style.SUCCESS("Successfully migrated 'default' database"))
        # 2. Iterate over all organizations
        # We need to ensure we are querying the 'default' DB for organizations
        # explicitly, although the router should handle it if DB_TYPE is 'main'.
        # But safest to be explicit if running from management command context where thread-local might be empty.
        
        orgs = Organization.objects.all()
        
        for org in orgs:
            slug = org.slug
            if not slug:
                self.stdout.write(self.style.WARNING(f"Skipping organization '{org.name}' with no slug"))
                continue
            
            self.stdout.write(f"Migrating organization '{slug}'...")
            # Ensure DB connection exists (simulating dynamic setup for SQLite)
            if slug not in settings.DATABASES:
                 new_db = settings.DATABASES['default'].copy()
                 new_db['NAME'] = settings.BASE_DIR / f"db/{slug}.sqlite3"
                 settings.DATABASES[slug] = new_db
            try:
                call_command('migrate', database=slug)
                self.stdout.write(self.style.SUCCESS(f"Successfully migrated '{slug}'"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to migrate '{slug}': {e}"))