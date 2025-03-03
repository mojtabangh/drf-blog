from django.db import transaction
from django.utils.text import slugify

from blog.models import Article
from users.models import User


@transaction.atomic
def create_article(*, title: str, content: str, author: User) -> Article:
    article = Article.objects.create(
        title=title,
        slug=slugify(title, allow_unicode=True),
        content=content,
        author=author
    )
    return article
