"""Các hàm / class dùng chung cho toàn bộ API (common hóa response + CRUD)."""
from rest_framework import permissions, views
from rest_framework.response import Response


def custom_response(message="", status="Success", data=None, status_code=200):
    body = {"status_code": status_code, "status": status, "message": message}
    if status == "Error":
        body["error"] = data
    else:
        body["data"] = data
    return Response(body, status=status_code)


class IsAdminOrReadOnly(permissions.BasePermission):
    """Ai cũng được đọc (GET), chỉ admin mới được ghi."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """Ai cũng được đọc, ghi thì phải đăng nhập."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)


class BaseListCreateView(views.APIView):
    """GET (list) + POST (create). Hỗ trợ resource con của một parent (vd: images của product)."""

    model = None
    serializer_class = None
    label = "item"
    parent_model = None   # vd: Product
    parent_field = None   # tên field FK trên model con, vd: 'product_id'
    parent_kwarg = None   # tên biến trên url, vd: 'product_id'

    # --- hooks ---
    def get_queryset(self, request, **kwargs):
        qs = self.model.objects.all()
        if self.parent_model:
            qs = qs.filter(**{self.parent_field: kwargs[self.parent_kwarg]})
        return qs

    def parent_queryset(self, request):
        return self.parent_model.objects.all()

    def extra_fields(self, request):
        return {}

    # --- handlers ---
    def get(self, request, **kwargs):
        if self.parent_model and not self.parent_queryset(request).filter(pk=kwargs[self.parent_kwarg]).exists():
            return custom_response("Parent not found!", "Error", None, 404)
        serializer = self.serializer_class(self.get_queryset(request, **kwargs), many=True)
        return custom_response(f"Get all {self.label}s successfully!", "Success", serializer.data, 200)

    def post(self, request, **kwargs):
        extra = self.extra_fields(request)
        if self.parent_model:
            parent = self.parent_queryset(request).filter(pk=kwargs[self.parent_kwarg]).first()
            if parent is None:
                return custom_response("Parent not found!", "Error", None, 404)
            extra[self.parent_field] = parent
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(**extra)
            return custom_response(f"Create {self.label} successfully!", "Success", serializer.data, 201)
        return custom_response(f"Create {self.label} failed!", "Error", serializer.errors, 400)


class BaseDetailView(views.APIView):
    """GET / PUT / DELETE một record theo pk."""

    model = None
    serializer_class = None
    label = "item"
    parent_field = None
    parent_kwarg = None

    def get_queryset(self, request, **kwargs):
        qs = self.model.objects.all()
        if self.parent_field:
            qs = qs.filter(**{self.parent_field: kwargs[self.parent_kwarg]})
        return qs

    def get_object(self, request, **kwargs):
        return self.get_queryset(request, **kwargs).filter(pk=kwargs["pk"]).first()

    def not_found(self):
        return custom_response(f"{self.label.capitalize()} not found!", "Error", None, 404)

    def get(self, request, **kwargs):
        obj = self.get_object(request, **kwargs)
        if obj is None:
            return self.not_found()
        return custom_response(f"Get {self.label} successfully!", "Success", self.serializer_class(obj).data, 200)

    def put(self, request, **kwargs):
        obj = self.get_object(request, **kwargs)
        if obj is None:
            return self.not_found()
        serializer = self.serializer_class(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return custom_response(f"Update {self.label} successfully!", "Success", serializer.data, 200)
        return custom_response(f"Update {self.label} failed!", "Error", serializer.errors, 400)

    def delete(self, request, **kwargs):
        obj = self.get_object(request, **kwargs)
        if obj is None:
            return self.not_found()
        obj.delete()
        # 204 không có body nên dùng 200 để client vẫn đọc được message
        return custom_response(f"Delete {self.label} successfully!", "Success", {"id": kwargs["pk"]}, 200)
