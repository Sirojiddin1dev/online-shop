from modeltranslation.translator import register, TranslationOptions, translator
from .models import *


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title','info',)


@register(Banner)
class BannerTranslationOptions(TranslationOptions):
    fields = ('banner_title','banner_description',)

@register(About)
class AboutTranslationOptions(TranslationOptions):
    fields = ('title','description',)


@register(Tag)
class TagTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Blog)
class BlogTranslationOptions(TranslationOptions):
    fields = ('title','text','text2',)
