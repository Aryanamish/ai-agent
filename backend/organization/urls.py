from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductsViewSet, OrganizationViewSet, BotSettingsViewSet

router = DefaultRouter()
router.register(r'organizations', OrganizationViewSet)
router.register(r'products', ProductsViewSet)
router.register(r'botsettings', BotSettingsViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
