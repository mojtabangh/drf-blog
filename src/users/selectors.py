from django.shortcuts import get_object_or_404

from .models import User


def get_user(pk: int) -> User:
    user = get_object_or_404(User, pk=pk)
    return user
