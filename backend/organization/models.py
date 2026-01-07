from django.db import models


# Create your models here.
class Organization(models.Model):
    DB_TYPE = 'main'
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    domain = models.CharField(max_length=255)
    required_attributes = models.JSONField()
    system_prompt = models.TextField()

    def __str__(self):
        return self.name

class BotSettings(models.Model):
    DB_TYPE = 'org'
    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255)
    required_attributes = models.JSONField()
    system_prompt = models.TextField()
    def __str__(self):
        return self.name


class Products(models.Model):
    DB_TYPE = 'org'
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    attributes = models.JSONField()
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    embedding = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name