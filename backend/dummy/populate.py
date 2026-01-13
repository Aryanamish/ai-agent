import logging
import os
import random
import sys
import urllib.request
from decimal import Decimal
from io import BytesIO
from urllib.error import URLError

import django

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Setup Django environment
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
sys.path.append(backend_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aichatbot.settings')
django.setup()

from django.core.files.base import ContentFile

from organization.models import Products


def populate():
    logger.info("Starting product population (Clothing Sector)...")

    # Seed data for generation
    clothing_types = [
        "T-Shirt", "Jeans", "Jacket", "Sweater", "Dress", 
        "Skirt", "Hoodie", "Blazer", "Scarf", "Coat",
        "Trousers", "Shorts", "Cardigan", "Vest", "Blouse"
    ]
    
    materials = [
        "Cotton", "Denim", "Leather", "Silk", "Wool", 
        "Linen", "Polyester", "Velvet", "Cashmere", "Satin"
    ]
    
    adjectives = [
        "Vintage", "Modern", "Classic", "Slim-fit", "Oversized", 
        "Casual", "Formal", "Luxury", "Urban", "Minimalist",
        "Chic", "Bohemian", "Retro", "Athletic", "Elegant"
    ]
    
    colors = [
        "Black", "White", "Navy", "Beige", "Charcoal", 
        "Olive", "Burgundy", "Cream", "Indigo", "Tan"
    ]

    # Curated list of high-quality fashion images from Unsplash
    # We use specific IDs to ensure the images exist and are relevant
    image_urls = [
        "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=800&q=80", # White tee
        "https://images.unsplash.com/photo-1542272617-08f086303294?w=800&q=80", # Patterned shirt
        "https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=800&q=80", # White button up
        "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=800&q=80", # Jacket
        "https://images.unsplash.com/photo-1551488852-080175b92789?w=800&q=80", # Coat
        "https://images.unsplash.com/photo-1543087903-1ac2ec7aa8c5?w=800&q=80", # Parka
        "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=800&q=80", # Fashion model
        "https://images.unsplash.com/photo-1529139574466-a302d2d3f52c?w=800&q=80", # Denim
        "https://images.unsplash.com/photo-1550246140-29f40b909e5a?w=800&q=80", # Hoodie
        "https://images.unsplash.com/photo-1582552938357-32b906df40cb?w=800&q=80", # Jeans
        "https://images.unsplash.com/photo-1548883354-94bcfe321cbb?w=800&q=80", # Sweater
        "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=800&q=80", # Black T-shirt
        "https://images.unsplash.com/photo-1550614000-4b9519e0037a?w=800&q=80", # Knitwear
        "https://images.unsplash.com/photo-1533659828811-0322d6475053?w=800&q=80", # Floral dress
        "https://images.unsplash.com/photo-1525459695603-514d33a9257e?w=800&q=80"  # Accessories
    ]

    target_count = 100
    created_count = 0

    while created_count < target_count:
        # Generate random attributes
        adj = random.choice(adjectives)
        mat = random.choice(materials)
        c_type = random.choice(clothing_types)
        color = random.choice(colors)
        
        # Construct Name
        name = f"{adj} {color} {mat} {c_type}"
        
        # Construct Description
        desc_templates = [
            f"A stunning {name.lower()} perfect for any occasion. Made from high-quality {mat.lower()}.",
            f"Elevate your style with this {adj.lower()} {c_type.lower()}. Features a comfortable fit and durable {mat.lower()} fabric.",
            f"The ultimate {c_type.lower()} in {color.lower()}. Designed for the modern individual who values both style and comfort.",
            f"Authentic {adj.lower()} design. This {mat.lower()} {c_type.lower()} is a must-have for your wardrobe this season."
        ]
        description = random.choice(desc_templates)

        # Generate Price (between 20.00 and 500.00)
        price = Decimal(random.uniform(20.0, 500.0)).quantize(Decimal("0.01"))
        
        # Pick a random image
        # In a real scenario, you might want to match image to type, but for volume testing, random is okay.
        image_url = random.choice(image_urls)

        # Check for duplicates based on name
        if Products.objects.filter(name=name).exists():
            continue

        try:
            logger.info(f"Creating product ({created_count + 1}/{target_count}): {name}")
            
            product = Products(
                name=name,
                price=price,
                description=description
            )
            
            # Download image
            # To speed up 100 entries, we might want to catch errors or be gentle
            # For this script we will try each time, but duplicates reuse the same URL so caching might happen at OS level or not at all.
            # Intentionally simplistic for this script.
            
            req = urllib.request.Request(
                image_url, 
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                img_content = response.read()
                # Create a filename
                img_name = f"{name.lower().replace(' ', '_')}_{random.randint(1000, 9999)}.jpg"
                product.image.save(img_name, ContentFile(img_content), save=False)
            
            product.save()
            created_count += 1

        except URLError as e:
            logger.error(f"Failed to download image for {name}: {e}")
            # Ensure we don't save broken records if image is critical, 
            # OR save without image if you prefer. 
            # Here we skip to try again or move on.
            pass 
        except Exception as e:
            logger.error(f"Error creating product {name}: {e}")

    logger.info(f"Population complete. Created {created_count} new entries.")

if __name__ == "__main__":
    populate()
