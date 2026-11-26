from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils import timezone

from products.models import Product


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    receiver_name = models.CharField(max_length=255)
    receiver_phone = models.CharField(max_length=15)
    receiver_address = models.CharField(max_length=255)
    is_ordered = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    total = models.FloatField(default=0)
    description = models.CharField(max_length=512, blank=True, default="")
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["created_at"])]


class OrderDetail(models.Model):
    id = models.AutoField(primary_key=True)
    amount = models.IntegerField()
    price = models.FloatField()
    discount = models.IntegerField(default=0)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_details")
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)


# Tự động cập nhật tổng tiền đơn hàng khi order detail được thêm / sửa / xóa
@receiver([post_save, post_delete], sender=OrderDetail)
def update_order_total(sender, instance, **kwargs):
    order = Order.objects.filter(pk=instance.order_id_id).first()
    if order is None:  # order đã bị xóa (cascade)
        return
    order.total = sum(
        (d.price - d.price * d.discount / 100) * d.amount for d in order.order_details.all()
    )
    order.save(update_fields=["total", "updated_at"])
