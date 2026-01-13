import json
import os
from datetime import datetime
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime

from aichatbot.utils import set_organization_slug
from organization.models import Products


class Command(BaseCommand):
    help = 'Load products from a JSON file into an organization database'

    def add_arguments(self, parser):
        parser.add_argument('--org', type=str, required=True, help='Organization slug')
        parser.add_argument('--input', type=str, required=True, help='Input JSON file path')

    def handle(self, *args, **options):
        org_slug = options['org']
        input_file = options['input']

        if not os.path.exists(input_file):
            self.stdout.write(self.style.ERROR(f'File not found: {input_file}'))
            return

        # Set the organization context
        set_organization_slug(org_slug)
        
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if not isinstance(data, list):
                self.stdout.write(self.style.ERROR('Invalid JSON format. Expected a list of products.'))
                return

            count = 0
            for item in data:
                # Basic validation can be added here
                
                # Convert types back
                price = Decimal(item.get('price', '0.00'))
                created_at_str = item.get('created_at')
                created_at = parse_datetime(created_at_str) if created_at_str else None
                
                Products.objects.create(
                    name=item.get('name'),
                    price=price,
                    attributes=item.get('attributes', {}),
                    image=item.get('image'),
                    created_at=created_at,
                    embedding=item.get('embedding')
                    # Note: ID is auto-generated. We are creating NEW records.
                    # If we wanted to sync/update, we'd need a unique identifier logic.
                )
                count += 1

            self.stdout.write(self.style.SUCCESS(f'Successfully loaded {count} products into organization "{org_slug}"'))

        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR(f'Invalid JSON in file: {input_file}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
