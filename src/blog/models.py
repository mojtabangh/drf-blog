from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model # noqa
from common.models import BaseModel


class Article(BaseModel):
    title = models.CharField(max_length=255, db_index=True,)
    slug = models.SlugField(max_length=255, db_index=True, allow_unicode=True,)
    content = models.TextField()
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self):
        return self.slug
