from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import *


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ["name", "description", "created_at", "updated_at"]
    search_fields = ["name", "description"]
    list_filter = ["created_at", "updated_at"]
    list_per_page = 10


@admin.register(Blog)
class BlogAdmin(TranslationAdmin):
    list_display = ["title", "category", "review_count", "created_at", "updated_at"]
    search_fields = ["title", "content", "category__name"]
    list_filter = ["category", "created_at", "updated_at"]
    list_per_page = 10
