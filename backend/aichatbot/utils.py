import threading
_thread_locals = threading.local()
def set_organization_slug(slug):
    _thread_locals.organization_slug = slug
def get_organization_slug():
    return getattr(_thread_locals, 'organization_slug', None)
def clear_organization_slug():
    if hasattr(_thread_locals, 'organization_slug'):
        del _thread_locals.organization_slug