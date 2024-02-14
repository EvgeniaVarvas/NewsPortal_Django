from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.conf import settings

from .forms import PostForm
from .models import Author, Post, Category

from django.http import HttpResponse
from django.views import View
from .tasks import hello, printer


class PostListMixin(ListView):
    model = Post
    post_type_filter = None
    ordering = '-created'
    paginate_by = 3

    def get_queryset(self):
        if isinstance(self.post_type_filter, list):
            return Post.objects.filter(post_type__in=self.post_type_filter).order_by('-created')
        else:
            return Post.objects.filter(post_type=self.post_type_filter).order_by('-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = context['object_list']
        return context


class NewsList(PostListMixin):
    post_type_filter = 'news'
    template_name = 'news/common_list.html'


class ArticleList(PostListMixin):
    post_type_filter = 'article'
    template_name = 'news/common_list.html'


class AllList(PostListMixin):
    post_type_filter = ['news', 'article']
    template_name = 'news/common_list.html'


class CategoryList(PostListMixin):
    post_type_filter = ['news', 'article']
    template_name = 'news/category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(categories=self.category).order_by('-created')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscribe'] = self.request.user not in self.category.subscribe.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    email = user.email
    category.subscribe.add(user)
    html = render_to_string(
        'news/subscribe.html', {
            'category': category,
            'user': user,
            'url': f'{settings.SITE_URL}categories/',
        },
    )
    msg = EmailMultiAlternatives(
        subject=f'Вы подписались на категорию {category}',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email, ],
    )
    msg.attach_alternative(html, 'text/html')
    try:
        msg.send()
    except Exception as e:
        print(e)
    return redirect('category_all')


@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribe.remove(user)
    return redirect('category_all')


@login_required
def get_category(request):
    user = request.user
    categories = Category.objects.all()
    category_info = []
    for category in categories:
        is_subscribed = user in category.subscribe.all()
        category_info.append({'category': category, 'is_subscribed': is_subscribed})
    return render(request, 'news/categories.html', {'categories': category_info})


class CreateNews(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    raise_exception = True
    template_name = 'news/create_news.html'

    def form_valid(self, form):
        author_instance, created = Author.objects.get_or_create(user=self.request.user)
        form.instance.author = author_instance
        return super().form_valid(form)


class PostDetail(DetailView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_detail.html'
    context_object_name = 'post_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = context['object']
        return context


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    model = Post
    form_class = PostForm
    template_name = 'news/create_news.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('news_list')


class SearchPost(ListView):
    model = Post
    template_name = 'news/common_list.html'
    context_object_name = 'search'

    def get_queryset(self):
        query = self.request.GET.get('q')
        results = Post.objects.filter(Q(title__iregex=query) | Q(text__iregex=query))
        return results

    def get_context_data(self, **kwargs: object) -> object:
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        context['news'] = self.get_queryset()
        return context


class IndexView(View):
    def get(self, request):
        # printer.apply_async([10],
        #                     eta=datetime.now() + timedelta(seconds=5))
        printer.apply_async([5], countdown=5)
        hello.delay()
        return HttpResponse('Hello!Hello!')
