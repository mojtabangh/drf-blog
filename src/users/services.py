from .models import User


def create_user(email: str, password: str, is_active: bool = True) -> User:
    user = User.objects.create(
        email=email,
        password=password,
        is_active=is_active,
    )

    return user
