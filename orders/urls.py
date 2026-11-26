from django.urls import path

from orders import views

urlpatterns = [
    path("orders/", views.OrderAPIView.as_view()),
    path("orders/<int:pk>/", views.OrderDetailAPIView.as_view()),
    path("orders/<int:order_id>/detail/", views.OrderDetailWithProductAPIView.as_view()),
    path("orders/<int:order_id>/detail/<int:pk>/", views.OrderDetailWithProductDetailAPIView.as_view()),
]
