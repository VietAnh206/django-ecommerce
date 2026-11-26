from rest_framework.permissions import AllowAny

from backend_ecommerce.helpers import (
    BaseDetailView,
    BaseListCreateView,
    IsAdminOrReadOnly,
    IsAuthenticatedOrReadOnly,
)

from .models import Category, Product, ProductComment, ProductImage
from .serializers import (
    CategorySerializer,
    ProductCommentSerializer,
    ProductImageSerializer,
    ProductSerializer,
)



class CategoryAPIView(BaseListCreateView):
    permission_classes = [IsAdminOrReadOnly]
    model = Category
    serializer_class = CategorySerializer
    label = "category"

    def get_queryset(self, request, **kwargs):
        return Category.objects.prefetch_related("products")


class CategoryDetailAPIView(BaseDetailView):
    permission_classes = [IsAdminOrReadOnly]
    model = Category
    serializer_class = CategorySerializer
    label = "category"


def _public_products(request):
    qs = Product.objects.prefetch_related("product_images", "product_comments")
    if not request.user.is_staff:
        qs = qs.filter(is_public=True)
    return qs


class ProductViewAPI(BaseListCreateView):
    """GET /product/?category=<id>&search=<text>"""

    permission_classes = [IsAdminOrReadOnly]
    model = Product
    serializer_class = ProductSerializer
    label = "product"

    def get_queryset(self, request, **kwargs):
        qs = _public_products(request)
        category = request.query_params.get("category")
        search = request.query_params.get("search")
        if category:
            qs = qs.filter(category_id=category)
        if search:
            qs = qs.filter(name__icontains=search)
        return qs


class ProductDetailAPIView(BaseDetailView):
    permission_classes = [IsAdminOrReadOnly]
    model = Product
    serializer_class = ProductSerializer
    label = "product"

    def get_queryset(self, request, **kwargs):
        return _public_products(request)


class ProductImageAPIView(BaseListCreateView):
    permission_classes = [IsAdminOrReadOnly]
    model = ProductImage
    serializer_class = ProductImageSerializer
    label = "product image"
    parent_model = Product
    parent_field = "product_id"
    parent_kwarg = "product_id"


class ProductImageDetailAPIView(BaseDetailView):
    permission_classes = [IsAdminOrReadOnly]
    model = ProductImage
    serializer_class = ProductImageSerializer
    label = "product image"
    parent_field = "product_id"
    parent_kwarg = "product_id"


class ProductCommentAPIView(BaseListCreateView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    model = ProductComment
    serializer_class = ProductCommentSerializer
    label = "product comment"
    parent_model = Product
    parent_field = "product_id"
    parent_kwarg = "product_id"

    def extra_fields(self, request):
        return {"user_id": request.user}


class ProductCommentDetailAPIView(BaseDetailView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    model = ProductComment
    serializer_class = ProductCommentSerializer
    label = "product comment"
    parent_field = "product_id"
    parent_kwarg = "product_id"

    def get_queryset(self, request, **kwargs):
        qs = super().get_queryset(request, **kwargs)
        # Chỉ chủ comment hoặc admin mới được sửa / xóa
        if request.method not in ("GET", "HEAD", "OPTIONS") and not request.user.is_staff:
            qs = qs.filter(user_id=request.user)
        return qs
