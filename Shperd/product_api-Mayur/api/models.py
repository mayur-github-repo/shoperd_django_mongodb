from django.db import models

# Create your models here.
from django.db import models


class Product(models.Model):
    class Meta:
        db_table = 'products'

    id = models.BigAutoField(primary_key=True)
    # id = models.BigIntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    handle = models.CharField(max_length=255)
    body_html = models.TextField()
    published_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    vendor = models.CharField(max_length=255)
    product_type = models.CharField(max_length=255)
    tags = models.TextField()

    def __str__(self):
        return self.title


class Image(models.Model):
    class Meta:
        db_table = 'images'
    created_at = models.DateTimeField()
    position = models.IntegerField()
    updated_at = models.DateTimeField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    variant_ids = models.TextField()
    src = models.CharField(max_length=255)
    width = models.IntegerField()
    height = models.IntegerField()


class Variant(models.Model):
    class Meta:
        db_table = 'variants'
    title = models.CharField(max_length=255)
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    sku = models.CharField(max_length=255)
    requires_shipping = models.BooleanField()
    taxable = models.BooleanField()
    featured_image = models.TextField()
    available = models.BooleanField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    grams = models.IntegerField()
    compare_at_price = models.DecimalField(max_digits=10, decimal_places=2)
    position = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
