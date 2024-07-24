from django.contrib import admin
from product.models import *
from modeltranslation.admin import TranslationAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _


# admin.site.register(Brand)

# admin.site.register(ProductVersion)
admin.site.register(ProductVersionImage)
# admin.site.register(Category)
# admin.site.register(ProductSubcategory)
# admin.site.register(ProductColor)
# admin.site.register(ProductTag)
admin.site.register(Discount)
admin.site.register(ProductSize)
# admin.site.register(Slider)
# admin.site.register(ProductDetail)



class ImageInline(admin.TabularInline):
    model = ProductVersionImage
    extra = 2


@admin.register(SpecialDiscount)
class SpecialDiscountAdmin(admin.ModelAdmin):
    list_display = ('id','product_version', 'discount_type', 'value', 'created_at', 'is_active')
    list_filter = ('created_at', 'discount_type')
    list_editable = ('value','product_version', 'is_active')
    search_fields = ('product_version__title',)


class SpecialDiscountInline(admin.TabularInline):
    model = SpecialDiscount
    extra = 1


@admin.register(ProductDetail)
class ProductDetailAdmin(TranslationAdmin):
    list_display = ['product', 'detail_type', 'value']
    list_filter = ['created_at']
    search_fields = ['product__title', 'detail_type__name', 'value']


# class ProductDetailInline(admin.StackedInline):  # Use StackedInline or TabularInline based on your preference
#     model = ProductDetail
#     can_delete = False  # Prevents deletion of associated ProductDetail when editing ProductVersion
#     verbose_name_plural = 'Product Details'  # Displayed name for the inline section

class ProductDetailInline(admin.TabularInline):  # Use StackedInline if you prefer a different layout
    model = ProductDetail
    extra = 1  # Number of empty forms to display
    # fields = ('detail_type', 'value')
    # readonly_fields = ('detail_type',)  # Make detail_type readonly if you want
    can_delete = True  # Allow deletion of product details from the inline form
    verbose_name_plural = 'Product Details'


@admin.register(ProductVersion)
class ProductAdmin(TranslationAdmin):
    # list_display = ('title', 'id', 'get_photo', 'price','discount', 'get_special_discount', 'get_discounted_price','brand',"category","get_main_cat", 'get_sizes' )
    list_display = ('id','title', 'get_photo', 'price','discount', 'get_special_discount', 'get_discounted_price' )
    list_filter = ["brand", "size", 'color', "category"]
    list_display_links = ['id', "title", "get_photo"] 
    # list_editable = ['price', "brand",  'discount', "category"]
    list_editable = ['price', 'discount']
    search_fields = ['title', 'description',  'brand__title', 'category__title' ]
    fieldsets = (
        ('info', {
            'fields': ('title',  'description', 'price','discount','stock','sales', 'display_image', 'cover_image','is_active','is_new', 'slug', 'created_at', "updated_at")
        }),
        ('relations', {
            'fields': ('category', 'brand', 'size','color' ,'tags', )
        }),
    )
    readonly_fields = ('display_image','created_at', "updated_at", 'slug', 'sales')
    inlines = [ImageInline, SpecialDiscountInline, ProductDetailInline]


    def get_sizes(self, obj):
        size_arr = [p.title for p in obj.size.all()]
        return size_arr
    get_sizes.short_description = 'Sizes'

    def get_special_discount(self, obj):
        special_discount = obj.special_discounts.filter(is_active=True).first()
        if special_discount:
            return f'{special_discount.value} {special_discount.discount_type}'
        else:
            return 'No Daily Special Discount'
    get_special_discount.short_description = 'Daily Special Discount'
    
    def get_main_cat(self, obj):
        if obj.category.parent_category:
            return obj.category.parent_category.title
        else:
            return obj.category.title
    get_main_cat.short_description = 'Main Category'
    
    
    def get_discounted_price(self, obj):
        return obj.get_discounted_price()
    get_discounted_price.short_description = 'Discounted Price'


    def get_photo(self, obj):
        if obj.cover_image:
            img_str = f"<img src='{obj.cover_image.url}' width='100px'>"
        return format_html(img_str)
    get_photo.short_description = 'Cover Image'

    def display_image(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" style="max-width: 300px; max-height: 300px;" />', obj.cover_image.url)
        return _("No Image Available")
    display_image.short_description = _('Cover Image')
    display_image.allow_tags = True

    def save_model(self, request, obj, form, change):
        # Check if the category exists for the given brand
        if obj.brand and obj.category:
            obj.category.brands.add(obj.brand)
        
        super().save_model(request, obj, form, change)



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


@admin.register(Category)
class ProductCategoryAdmin(TranslationAdmin):
    list_display = ["id", "title", "get_photo", "get_parent_category", "get_brands"]
    list_display_links = ['id', "title", "get_photo"] 
    # list_editable = ["is_active"]
    list_per_page = 10

    def get_brands(self, obj):
        # If the category is a main category
        if not obj.parent_category:
            if obj.child_cats.all():
                # Gather brands of the subcategories
                brands = set(obj.brands.all())
                for subcategory in obj.child_cats.all():
                    brands.update(subcategory.brands.all())
            else:
                brands = obj.brands.all()
        else:
            # Only gather brands of the current category if it is a subcategory
            brands = obj.brands.all()
        
        # Create a string of brand titles separated by commas
        brands_str = ", ".join(brand.title for brand in brands)
        return brands_str
    get_brands.short_description = 'Brands'
    

    def get_parent_category(self, obj):
        return obj.get_parent()
    get_parent_category.short_description = 'Main Category'

    def get_photo(self, obj):
        if obj.icon:
            img_str = f"<img src='{obj.icon.url}' width='100px'>"
            return format_html(img_str)
        return "No Icon"
    get_photo.short_description = 'Icon'


# @admin.register(ProductSubcategory)
# class ProductSubcategoryAdmin(TranslationAdmin):
#     list_display = ["id", "title", "category"]
#     list_display_links = ['id', "title"] 
#     list_editable = ["category"]
#     list_per_page = 10


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



@admin.register(ProductDetailType)
class ProductDetailTypeAdmin(TranslationAdmin):
    list_display = ["name"]

