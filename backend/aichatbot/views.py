from django.conf import settings
from django.contrib import admin
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.http import JsonResponse


class CustomAdminLoginView(LoginView):
    template_name = "admin/login.html"

    def get_success_url(self):
        # Force redirect to LOGIN_REDIRECT_URL even if 'next' parameter is present
        return settings.LOGIN_REDIRECT_URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "site_header": admin.site.site_header,
            "site_title": admin.site.site_title,
            "site_url": admin.site.site_url,
            "has_permission": True,
            "available_apps": admin.site.get_app_list(self.request),
        })
        return context


def getCurrentUser(request):
    
    if request.user.is_authenticated:
        return JsonResponse({
            "username": request.user.username,
            "email": request.user.email,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
        }, status=200)
    return JsonResponse({"error": "Not authenticated"}, status=401)


def logoutUser(request):
    """Logout the current user and clear the session."""
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({"message": "Successfully logged out"}, status=200)
    return JsonResponse({"error": "Not authenticated"}, status=401)


def health_check(request):
    """Health check endpoint for Docker/Kubernetes."""
    return JsonResponse({"status": "healthy"}, status=200)