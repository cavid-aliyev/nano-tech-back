from django.contrib import admin
from product.models import *
from django.utils.html import format_html



# admin.site.register(Brand)

admin.site.register(ProductVersion)
admin.site.register(ProductVersionImage)
admin.site.register(ProductCategory)
admin.site.register(ProductSubcategory)
admin.site.register(ProductColor)
admin.site.register(ProductTag)
admin.site.register(Discount)
admin.site.register(ProductSize)
# admin.site.register(Slider)


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


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "get_photo", "is_active"]
    list_display_links = ['id', "title", "get_photo"] 
    list_editable = ["is_active"]
    # list_per_page = 10

    def get_photo(self, obj):
        if obj.image:
            img_str = f"<img src='{obj.image.url}' width='100px'>"
        return format_html(img_str)


@admin.register(TopBrand)
class TopBrandAdmin(admin.ModelAdmin):
    list_display = ["id", "get_photo", "is_active"]
    list_display_links = ['id', "get_photo"] 
    list_editable = ["is_active"]
    # list_per_page = 10

    def get_photo(self, obj):
        if obj.image:
            img_str = f"<img src='{obj.image.url}' width='100px'>"
        return format_html(img_str)
