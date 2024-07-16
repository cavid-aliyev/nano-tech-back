from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from django.utils.html import format_html
from home.models import Slider

# Register your models here.

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ["id", "get_photo", "is_active", "created_at", "updated_at"]
    list_filter = ["created_at", "updated_at"]
    list_display_links = ['get_photo', 'id'] 
    list_editable = ["is_active"]
    # list_per_page = 10

    def get_photo(self, obj):
        if obj.slider_image:
            img_str = f"<img src='{obj.slider_image.url}' width='100px'>"
        return format_html(img_str)
