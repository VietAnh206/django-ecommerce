from django.urls import path

from user import views

urlpatterns = [
    path("users/profile/", views.UserProfileView.as_view()),
]
