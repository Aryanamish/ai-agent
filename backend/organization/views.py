from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import Products, Organization
from .serializers import ProductsSerializer, OrganizationSerializer

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAdminUser]

class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    # Using AllowAny for demonstration ease as per "let me add the product" request
    # In production, this should likely be specific permissions
    permission_classes = [IsAdminUser]
