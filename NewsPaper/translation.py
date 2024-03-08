from news.models import Post
from modeltranslation.translator import register, TranslationOptions


# регистрируем наши модели для перевода

@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'text',)  # указываем, какие именно поля надо переводить в виде кортежа
