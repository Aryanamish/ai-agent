from django.urls import get_script_prefix, set_script_prefix
from django.utils.deprecation import MiddlewareMixin

from organization.models import Organization

from .utils import clear_organization_slug, set_organization_slug


class OrganizationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Capture current script prefix for cleanup
        request._old_script_prefix = get_script_prefix()

        # Extract slug from URL path
        path_segments = request.path_info.strip("/").split("/")

        if path_segments:
            slug = path_segments[0]
            # Check if organization exists
            if slug and Organization.objects.filter(slug=slug).exists():
                set_organization_slug(slug)

                # Remove the organization slug from the URL
                prefix = f"/{slug}"
                if request.path_info.startswith(prefix):
                    # Update SCRIPT_NAME in META for WSGI compatibility
                    request.META["SCRIPT_NAME"] = (
                        request.META.get("SCRIPT_NAME") or ""
                    ) + prefix

                    # Update Django's internal script prefix for reverse()
                    set_script_prefix(request.META["SCRIPT_NAME"])

                    new_path = request.path_info[len(prefix) :]
                    # Ensure path starts with /
                    if not new_path.startswith("/"):
                        new_path = "/" + new_path
                    request.path_info = new_path
            else:
                clear_organization_slug()
        else:
            clear_organization_slug()

    def process_response(self, request, response):
        if hasattr(request, "_old_script_prefix"):
            set_script_prefix(request._old_script_prefix)
        clear_organization_slug()
        return response

    def process_exception(self, request, exception):
        if hasattr(request, "_old_script_prefix"):
            set_script_prefix(request._old_script_prefix)
        clear_organization_slug()