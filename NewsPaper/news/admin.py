from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Author, Category, Post, Comment


class PostAdmin(TranslationAdmin):
    model = Post
    list_display = ('title', 'author', 'created', 'get_categories')
    list_filter = ('created', 'author', 'categories')
    search_fields = ('created', 'author', 'categories')

    def get_categories(self, obj):  # Определение метода get_categories
        return ", ".join([category.name for category in obj.categories.all()])

    get_categories.short_description = 'Categories'  # Даем короткое описание для поля в админке


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post_title', 'user', 'created', 'rating')
    list_filter = ('created', 'post__title', 'user')
    search_fields = ('created', 'post__title', 'user__username')

    def post_title(self, obj):
        return obj.post.title


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating')
    list_filter = ('user', 'rating')
    search_fields = ('user', 'rating')


class CategoryAdmin(TranslationAdmin):
    model = Category
    list_display = ('name', 'subscriber_count')
    list_filter = ('name',)
    search_fields = ('name',)

    def subscriber_count(self, obj):
        return obj.subscribe.count()  # Возвращает количество подписчиков на категорию

    subscriber_count.short_description = 'Subscribers'


admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, PostAdmin)
