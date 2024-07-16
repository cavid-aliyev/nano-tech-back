from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from django.utils.html import format_html
from banner.models import Banner

# Register your models here.


@admin.register(Banner)
class BannerAdmin(TranslationAdmin):
    list_display = ["id", "title", "description", "is_active", "created_at", "updated_at"]
    list_filter = ["created_at", "updated_at"]
    list_display_links = ['title', 'id'] 
    list_editable = ["is_active"]
    # list_per_page = 10