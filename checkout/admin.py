from django.contrib import admin
from checkout.models import WishlistItem
from django.contrib import admin
from .models import ShoppingCart, CartItem, BillingAddress

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0  # Do not show extra empty forms by default
    readonly_fields = ('get_total',)

@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'updated_at', 'get_total')
    # list_editable = ['get_user']
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username',)
    readonly_fields = ('created_at', 'updated_at', 'get_total')
    inlines = [CartItemInline]

    # def get_user(self, obj):
    #     return obj.user.get_full_name()
    # get_user.short_description = 'User'

    def get_total(self, obj):
        return obj.get_total
    get_total.short_description = 'Total'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product_version', 'quantity', 'created_at', 'updated_at', 'get_total')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('cart__user__username', 'product_version__title')
    readonly_fields = ('created_at', 'updated_at', 'get_total')

    def get_total(self, obj):
        return obj.get_total
    get_total.short_description = 'Total'

@admin.register(BillingAddress)
class BillingAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name', 'company_name', 'address', 'city', 'country', 'email', 'phone_number', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'country')
    search_fields = ('user__username', 'first_name', 'last_name', 'email', 'phone_number', 'address', 'city', 'company_name')
    readonly_fields = ('created_at', 'updated_at')

# Optionally, you can customize the display of ProductVersion in the admin if it's relevant to your app
# from product.models import ProductVersion
# @admin.register(ProductVersion)
# class ProductVersionAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title', 'price', 'created_at', 'updated_at')
#     list_filter = ('created_at', 'updated_at')
#     search_fields = ('title',)
#     readonly_fields = ('created_at', 'updated_at')


@admin.register(WishlistItem)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('id','product','product_id','user')
    list_filter = ["product", "user"]
    list_editable = ['product', 'user']
    list_display_links = ['id']   # oldugu columnlari kliklenen edir (link)

    def product_id(self, obj):
        if obj.product:
            return obj.product.id
        return None
