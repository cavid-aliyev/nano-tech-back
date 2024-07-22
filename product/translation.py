from modeltranslation.translator import translator, TranslationOptions, register
from product.models import Brand, Category,  ProductVersion, ProductColor, ProductTag, ProductSize, ProductDetailType, ProductDetail


@register(Brand)
class BrandTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(ProductDetailType)
class ProductDetailTypeTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(ProductDetail)
class ProductDetailTranslationOptions(TranslationOptions):
    fields = ('value',)


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title',)

# @register(ProductSubcategory)
# class ProductSubcategoryTranslationOptions(TranslationOptions):
#     fields = ('title',)


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
