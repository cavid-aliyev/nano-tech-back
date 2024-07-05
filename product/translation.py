from modeltranslation.translator import translator, TranslationOptions, register
from product.models import Brand, ProductCategory, ProductSubcategory, ProductVersion, ProductColor, ProductTag, ProductSize


@register(Brand)
class BrandTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(ProductCategory)
class ProductCategoryTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(ProductSubcategory)
class ProductSubcategoryTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(ProductColor)
class ProductColorTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(ProductTag)  
class ProductTagTranslationOptions(TranslationOptions):
    fields = ('title',)

# @register(ProductSize)
# class ProductSizeTranslationOptions(TranslationOptions):
#     fields = ('title',)


@register(ProductVersion)
class ProductVersionTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)

# translator.register(Brand, BrandTranslationOptions)
# translator.register(ProductCategory, ProductCategoryTranslationOptions)
# translator.register(ProductSubcategory, ProductSubcategoryTranslationOptions)
# translator.register(ProductVersion, ProductVersionTranslationOptions)
