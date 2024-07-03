from modeltranslation.translator import translator, TranslationOptions, register
from blog.models import Blog, Category


@register(Blog)
class BlogTranslationOptions(TranslationOptions):
    fields = ('title', "content")


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', "description")

    
# translator.register(Blog, BlogTranslationOptions)