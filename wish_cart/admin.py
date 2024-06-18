from django.contrib import admin
from wish_cart.models import WishlistItem



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
