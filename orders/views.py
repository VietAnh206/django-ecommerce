from rest_framework.permissions import IsAuthenticated

from backend_ecommerce.helpers import BaseDetailView, BaseListCreateView

from .models import Order, OrderDetail
from .serializers import OrderDetailSerializer, OrderSerializer


def _own_orders(request):
    """Admin thấy tất cả đơn, user thường chỉ thấy đơn của mình."""
    qs = Order.objects.prefetch_related("order_details")
    return qs if request.user.is_staff else qs.filter(user_id=request.user)


class OrderAPIView(BaseListCreateView):
    permission_classes = [IsAuthenticated]
    model = Order
    serializer_class = OrderSerializer
    label = "order"

    def get_queryset(self, request, **kwargs):
        return _own_orders(request)

    def extra_fields(self, request):
        return {"user_id": request.user}


class OrderDetailAPIView(BaseDetailView):
    permission_classes = [IsAuthenticated]
    model = Order
    serializer_class = OrderSerializer
    label = "order"

    def get_queryset(self, request, **kwargs):
        return _own_orders(request)


class OrderDetailWithProductAPIView(BaseListCreateView):
    permission_classes = [IsAuthenticated]
    model = OrderDetail
    serializer_class = OrderDetailSerializer
    label = "order detail"
    parent_model = Order
    parent_field = "order_id"
    parent_kwarg = "order_id"

    def parent_queryset(self, request):
        return _own_orders(request)


class OrderDetailWithProductDetailAPIView(BaseDetailView):
    permission_classes = [IsAuthenticated]
    model = OrderDetail
    serializer_class = OrderDetailSerializer
    label = "order detail"
    parent_field = "order_id"
    parent_kwarg = "order_id"

    def get_queryset(self, request, **kwargs):
        qs = super().get_queryset(request, **kwargs)
        return qs if request.user.is_staff else qs.filter(order_id__user_id=request.user)
