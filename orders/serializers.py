from rest_framework import serializers

from .models import Order, OrderDetail


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = "__all__"
        read_only_fields = ("order_id",)
        extra_kwargs = {
            "amount": {"min_value": 1},
            "price": {"required": False},     
            "discount": {"required": False},  
        }

    def create(self, validated_data):
        product = validated_data["product_id"]
        validated_data.setdefault("price", product.price)
        validated_data.setdefault("discount", product.discount)
        return super().create(validated_data)


class OrderSerializer(serializers.ModelSerializer):
    order_details = OrderDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ("user_id", "total", "is_paid")
