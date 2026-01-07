from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductsViewSet, OrganizationViewSet

router = DefaultRouter()
router.register(r'organizations', OrganizationViewSet)
router.register(r'products', ProductsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
