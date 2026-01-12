import json

from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    SAFE_METHODS,
    BasePermission,
)

from .models import BotSettings, Organization, Products
from .serializers import (
    BotSettingsSerializer,
    OrganizationSerializer,
    ProductListSerializer,
    ProductsSerializer,
)


class IsAdminOrReadOnly(BasePermission):
    """
    Allow read-only access to authenticated users, but require admin for edit operations.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_staff


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'


class BotSettingsViewSet(viewsets.ModelViewSet):
    queryset = BotSettings.objects.all()
    serializer_class = BotSettingsSerializer
    permission_classes = [IsAdminUser]


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer
        return ProductsSerializer

    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardResultsSetPagination
