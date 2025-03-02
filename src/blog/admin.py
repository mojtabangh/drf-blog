from django.contrib import admin

from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author")
    prepopulated_fields = {"slug": ["title"]}
    ordering = ("-updated_at",)
