from django.urls import path

from .apis import (
    UserRegisterApi,
)

app_name = 'users'

urlpatterns = [
    path("register/", UserRegisterApi.as_view(), name="user-register"),
]
