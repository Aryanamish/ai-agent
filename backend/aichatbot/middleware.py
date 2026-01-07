from django.utils.deprecation import MiddlewareMixin
from .utils import set_organization_slug, clear_organization_slug
from organization.models import Organization

class OrganizationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Extract slug from URL path
        path_segments = request.path_info.strip('/').split('/')
        
        if path_segments:
            slug = path_segments[0]
            # Check if organization exists
            if slug and Organization.objects.filter(slug=slug).exists():
                set_organization_slug(slug)
                
                # Remove the organization slug from the URL
                prefix = f"/{slug}"
                if request.path_info.startswith(prefix):
                    new_path = request.path_info[len(prefix):]
                    # Ensure path starts with /
                    if not new_path.startswith('/'):
                        new_path = '/' + new_path
                    request.path_info = new_path
            else:
                clear_organization_slug()
        else:
            clear_organization_slug()
            
    def process_response(self, request, response):
        clear_organization_slug()
        return response
    def process_exception(self, request, exception):
        clear_organization_slug()