import json
import os
from datetime import datetime
from decimal import Decimal

from django.conf import settings
from django.core.management.base import BaseCommand

from aichatbot.utils import set_organization_slug
from organization.models import Products


class Command(BaseCommand):
    help = 'Dump products from an organization database to a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('--org', type=str, required=True, help='Organization slug')
        parser.add_argument('--output', type=str, required=True, help='Output JSON file path')

    def handle(self, *args, **options):
        org_slug = options['org']
        output_file = options['output']

        # Set the organization context
        set_organization_slug(org_slug)

        # Trigger DB router logic to ensure DB is configured
        # We can do this by just accessing the DB, but set_organization_slug + accessing model should work
        # based on the router logic we read.
        
        try:
            products = Products.objects.all()
            data = []
            
            self.stdout.write(f"Fetching products for organization: {org_slug}")

            for product in products:
                item = {
                    'name': product.name,
                    'price': str(product.price), # Decimal to string
                    'attributes': product.attributes,
                    'image': product.image,
                    'created_at': product.created_at.isoformat() if product.created_at else None,
                }
                data.append(item)

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            self.stdout.write(self.style.SUCCESS(f'Successfully dumped {len(data)} products to "{output_file}"'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
