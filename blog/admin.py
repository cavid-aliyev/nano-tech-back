from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from django.utils.html import format_html

from .models import *


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ["name", "description", "created_at", "updated_at"]
    search_fields = ["name", "description"]
    list_filter = ["created_at", "updated_at"]
    list_per_page = 10


@admin.register(Blog)
class BlogAdmin(TranslationAdmin):
    list_display = ['id',"title", 'get_photo', "category", "review_count", "created_at", "updated_at"]
    search_fields = ["title", "content", "category__name"]
    list_display_links = ['id', "title", 'get_photo']
    list_filter = ["category", "created_at", "updated_at"]
    list_per_page = 10

    def get_photo(self, obj):
        if obj.image:
            img_str = f"<img src='{obj.image.url}' width='100px'>"
        return format_html(img_str)
    get_photo.short_description = 'Cover Image'
