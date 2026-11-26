from django.urls import path

from products import views

urlpatterns = [
    path("category/", views.CategoryAPIView.as_view()),
    path("category/<int:pk>/", views.CategoryDetailAPIView.as_view()),

    path("product/<int:product_id>/images/", views.ProductImageAPIView.as_view()),
    path("product/<int:product_id>/images/<int:pk>/", views.ProductImageDetailAPIView.as_view()),

    path("product/<int:product_id>/comments/", views.ProductCommentAPIView.as_view()),
    path("product/<int:product_id>/comments/<int:pk>/", views.ProductCommentDetailAPIView.as_view()),

    path("product/", views.ProductViewAPI.as_view()),
    path("product/<int:pk>/", views.ProductDetailAPIView.as_view()),
]
