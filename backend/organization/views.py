from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import Organization, Products
from .serializers import (
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

class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer
        return ProductsSerializer

    # Using AllowAny for demonstration ease as per "let me add the product" request
    # In production, this should likely be specific permissions
    permission_classes = [IsAdminUser]
    pagination_class = StandardResultsSetPagination
