from modeltranslation.translator import translator, TranslationOptions, register
from banner.models import Banner


@register(Banner)
class BannerTranslationOptions(TranslationOptions):
    fields = ('title',"description")

