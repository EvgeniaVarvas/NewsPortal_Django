from django import forms
from .models import Category, Post, PostCategory



class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'text', 'post_type', 'categories']
        labels = {
            'title': 'Заголовок',
            'text': 'Текст',
            'post_type': 'Тип',
            'categories': 'Категории',
        }
