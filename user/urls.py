from django.urls import path
from .views import RegisterView, MeView


app_name = "user"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("me/", MeView.as_view(), name="me")
]
