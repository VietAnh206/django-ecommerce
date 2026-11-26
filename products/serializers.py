from rest_framework import serializers

from . import models


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = "__all__"
        read_only_fields = ("product_id",)


class ProductCommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user_id.username", read_only=True)

    class Meta:
        model = models.ProductComment
        fields = "__all__"
        read_only_fields = ("product_id", "user_id")


class ProductSerializer(serializers.ModelSerializer):
    # source phải trùng related_name khai báo trong model
    images = ProductImageSerializer(source="product_images", many=True, read_only=True)
    comments = ProductCommentSerializer(source="product_comments", many=True, read_only=True)

    class Meta:
        model = models.Product
        fields = (
            "id", "name", "unit", "price", "discount", "amount", "is_public",
            "thumbnail", "description", "images", "comments", "category_id",
            "created_at", "updated_at", "deleted_at",
        )


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = models.Category
        fields = ("id", "name", "slug", "icon_url", "products", "created_at", "updated_at", "deleted_at")
