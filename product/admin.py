from django.contrib import admin
from product.models import *
from modeltranslation.admin import TranslationAdmin
from django.utils.html import format_html



# admin.site.register(Brand)

# admin.site.register(ProductVersion)
admin.site.register(ProductVersionImage)
# admin.site.register(ProductCategory)
# admin.site.register(ProductSubcategory)
# admin.site.register(ProductColor)
# admin.site.register(ProductTag)
admin.site.register(Discount)
admin.site.register(ProductSize)
# admin.site.register(Slider)



class ImageInline(admin.TabularInline):
    model = ProductVersionImage
    extra = 2



@admin.register(ProductVersion)
class ProductAdmin(TranslationAdmin):
    list_display = ('title', 'id', 'get_photo','brand','subcategory', 'price','discount', 'get_discounted_price', 'get_cat','get_sizes' )
    list_filter = ["subcategory", "brand", "size", 'color']
    list_display_links = ['id', "title", "get_photo"] 
    list_editable = ['price', "brand", 'subcategory', 'discount']
    search_fields = ['title', 'description', 'subcategory__title', 'brand__title']
    # fieldsets = (
    #     ('info', {
    #         'fields': ('title', 'cover_image',  'description','price', 'slug')
    #     }),
    #     ('relations', {
    #         'fields': ('subcategory', 'brand', 'size','color' ,'tags')
    #     }),
    # )
    inlines = [ImageInline]


    def get_sizes(self, obj):
        size_arr = [p.title for p in obj.size.all()]

        return size_arr
    
    def get_cat(self, obj):
        return obj.subcategory.category.title


    def get_photo(self, obj):
        if obj.cover_image:
            img_str = f"<img src='{obj.cover_image.url}' width='100px'>"
        return format_html(img_str)



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
class BrandAdmin(TranslationAdmin):
    list_display = ["id", "title", "get_photo", "is_active"]
    list_display_links = ['id', "title", "get_photo"] 
    list_editable = ["is_active"]
    # list_per_page = 10

    def get_photo(self, obj):
        if obj.image:
            img_str = f"<img src='{obj.image.url}' width='100px'>"
        return format_html(img_str)


@admin.register(ProductCategory)
class ProductCategoryAdmin(TranslationAdmin):
    list_display = ["id", "title", "get_subcats" ,"is_active"]
    list_display_links = ['id', "title"] 
    list_editable = ["is_active"]
    list_per_page = 10

    def get_subcats(self, obj):
        subcats_arr = [p.title for p in obj.subcategories.all()]

        return subcats_arr


@admin.register(ProductSubcategory)
class ProductSubcategoryAdmin(TranslationAdmin):
    list_display = ["id", "title", "category"]
    list_display_links = ['id', "title"] 
    list_editable = ["category"]
    list_per_page = 10


@admin.register(ProductColor)
class ProductColorAdmin(TranslationAdmin):
    list_display = ["id", "title", "hex_code", "is_active"]
    list_display_links = ['id', "title", "hex_code"] 
    list_editable = ["is_active"]
    # list_per_page = 10


@admin.register(ProductTag)
class ProductTagAdmin(TranslationAdmin):
    list_display = ["id", "title",  "is_active"]
    list_display_links = ['id', "title"] 
    list_editable = ["is_active"]
    # list_per_page = 10



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
