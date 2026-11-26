from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)
    icon_url = models.CharField(max_length=128, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)  

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=10)
    price = models.FloatField()
    discount = models.IntegerField(default=0)  
    amount = models.IntegerField(default=0)    
    is_public = models.BooleanField(default=True)
    thumbnail = models.CharField(max_length=255, blank=True, default="")
    description = models.TextField(blank=True, default="")
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["created_at"])]

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    id = models.AutoField(primary_key=True)
    image_url = models.CharField(max_length=255)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_images")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)


class ProductComment(models.Model):
    id = models.AutoField(primary_key=True)
    rating = models.IntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.CharField(max_length=512)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_comments")
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # comment gốc: parent_id = null; comment trả lời: parent_id = id comment gốc
    parent_id = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
