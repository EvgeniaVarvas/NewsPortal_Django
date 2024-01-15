from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        article_rating = Post.objects.filter(author=self).aggregate(Sum('rating'))['rating__sum'] or 0
        article_rating *= 3
        comment_rating = Comment.objects.filter(user=self.user).aggregate(Sum('rating'))['rating__sum'] or 0
        article_comment_rating = Comment.objects.filter(post__author=self).aggregate(Sum('rating'))['rating__sum'] or 0
        
        self.rating = article_rating + comment_rating + article_comment_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    post_type = models.CharField(max_length=10, choices=[('article', 'Статья'), ('news', 'Новость')])
    created = models.DateTimeField(auto_now_add = True)
    categories = models.ManyToManyField('Category', through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def preview(self):
        return self.text[:20] + '...'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.title}. {self.text} Автор: {self.author.user}'  
    
    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.pk)])


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add = True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
