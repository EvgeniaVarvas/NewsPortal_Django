from django import forms
from .models import Category, Post



class PostForm(forms.ModelForm):
    categories = forms.ModelChoiceField(
    queryset=Category.objects.all(),
    label = 'Категория',
    empty_label='Select')
    class Meta:
        model = Post
        fields = ['title', 'text', 'post_type']
        labels = {
            'title': 'Заголовок',
            'text': 'Текст',
            'post_type': 'Тип',
        }

# class PostForm(forms.ModelForm):
  
#     class Meta:
#         model = Post
#         fields = '__all__'
        
        