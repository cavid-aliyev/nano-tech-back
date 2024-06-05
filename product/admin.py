from django.contrib import admin
from product.models import *


admin.site.register(Brand)

admin.site.register(ProductVersion)
admin.site.register(ProductVersionImage)
admin.site.register(ProductCategory)
admin.site.register(ProductSubcategory)
admin.site.register(ProductColor)
admin.site.register(ProductTag)
admin.site.register(Discount)
admin.site.register(ProductSize)