import json

from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser

from .models import BotSettings, Organization, Products
from .serializers import (
    BotSettingsSerializer,
    OrganizationSerializer,
    ProductListSerializer,
    ProductsSerializer,
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAdminUser]


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

    permission_classes = [IsAdminUser]
    pagination_class = StandardResultsSetPagination
