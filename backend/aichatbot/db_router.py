from django.conf import settings
from .utils import get_organization_slug
class OrganizationRouter:
    def db_for_read(self, model, **hints):
        return self._get_db(model)
    def db_for_write(self, model, **hints):
        return self._get_db(model)
    def allow_relation(self, obj1, obj2, **hints):
        # Allow if both are in 'default' or both are in same org DB
        db1 = self._get_db(obj1._meta.model)
        db2 = self._get_db(obj2._meta.model)
        if db1 and db2 and db1 == db2:
            return True
        return None
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if model_name:
             # We need to import the model class to check DB_TYPE
             # However, 'model_name' is just a string here. 
             # 'hints' might contain 'model' class in some django versions, but safer to rely on app/model lookup or strict check.
             # Actually, simpler approach:
             # We want strict separation. 
             # 'default' DB contains only 'main' models.
             # 'org' DBs contain only 'org' models.
             
             # To do this safely without importing everything, we can rely on looking up the model from apps.
             from django.apps import apps
             try:
                 model = apps.get_model(app_label, model_name)
                 db_type = getattr(model, 'DB_TYPE', 'main')
             except LookupError:
                 return None
             if db == 'default':
                 return db_type == 'main'
             else:
                 return db_type == 'org'
        return None
    def _get_db(self, model):
        db_type = getattr(model, 'DB_TYPE', 'main')
        
        if db_type == 'main':
            return 'default'
        
        if db_type == 'org':
            slug = get_organization_slug()
            if not slug:
                raise Exception(
                    f"Attempting to access organization model '{model.__name__}' "
                    "without an active organization context (slug)."
                )
            
            # Ensure the database connection exists in settings
            if slug not in settings.DATABASES:
                 # In a real dynamic scenario, we might add it here for SQLite
                 # But sticking to the plan, we expect it to be there or we fail.
                 # Wait, for the 'migrate_all' command we'll add it.
                 # For runtime requests, we need to ensure it's added.
                 # Let's add simple dynamic SQLite logic here for development convenience as noted in plan.
                 new_db = settings.DATABASES['default'].copy()
                 new_db['NAME'] = settings.BASE_DIR / f"db/{slug}.sqlite3"
                 settings.DATABASES[slug] = new_db
            
            return slug
        
        return 'default'