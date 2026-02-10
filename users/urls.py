from django.urls import path
from users.apps import UsersConfig
from .views import (
    RegisterView,
    CustomUserRetrieveAPIView,
    CustomUserUpdateAPIView,
    CustomUserDestroyAPIView,
)
from django.contrib.auth.views import LoginView, LogoutView

app_name = UsersConfig.name

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="study:home"), name="logout"),
    path("profile/", CustomUserRetrieveAPIView.as_view(), name="profile"),
    path("profile/edit", CustomUserUpdateAPIView.as_view(), name="profile-edit"),
    path("profile/delete", CustomUserDestroyAPIView.as_view(), name="profile-delete"),
]
