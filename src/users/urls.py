from django.urls import path

from .apis import (
    UserRegisterApi,
)

urlpatterns = [
    path("register/", UserRegisterApi.as_view(), name="user-register"),
]
