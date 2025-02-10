from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import ASCIIUsernameValidator
from django.core.validators import MinLengthValidator
from django.utils import timezone
from django.core.mail import send_mail

from common.models import BaseModel


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    """ eh """
    username_validator = ASCIIUsernameValidator()
    email = models.EmailField(
        max_length=255,
        unique=True,
        db_index=True,
    )
    username = models.CharField(
        max_length=20,
        validators=[
            MinLengthValidator(6),
            username_validator,
        ],
        unique=True,
        db_index=True
    )

    is_staff = models.BooleanField(default=False,)
    is_active = models.BooleanField(default=True,)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return ...
