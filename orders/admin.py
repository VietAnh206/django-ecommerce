from django.contrib import admin

from .models import Order, OrderDetail


class OrderDetailInline(admin.TabularInline):
    model = OrderDetail
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "receiver_name", "total", "is_ordered", "is_paid", "created_at")
    inlines = [OrderDetailInline]
