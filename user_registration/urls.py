from django.urls import path

from .views import (
    RegisterUserAPIView,
    LoginAPIView,
    LogoutView
)

app_name = "user_registration"
urlpatterns = [
    path("register/", view=RegisterUserAPIView.as_view(), name="register"),
    path("login/", view=LoginAPIView.as_view(), name="login"),
    path("logout/", view=LogoutView.as_view(), name="logout"),
]
