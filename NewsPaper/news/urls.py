from django.urls import path
from .views import (ArticleList, CreateNews, NewsList, PostDetail,
                    PostUpdate, PostDelete, AllList, SearchPost, get_category, CategoryList, subscribe, unsubscribe,
                    IndexView
                    )

# subscribe, unsubscribe,

urlpatterns = [
    path('category_list/<int:pk>/', CategoryList.as_view(), name='category_list'),
    path('', AllList.as_view(), name='all_list'),
    path('search/', SearchPost.as_view(), name='product_search'),
    path('news/', NewsList.as_view(), name='news_list'),
    path('article/', ArticleList.as_view(), name='article_list'),
    path('create_news/', CreateNews.as_view(), name='create_news'),
    path('post_detail/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('create_news/<int:pk>/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('subscribe/<int:pk>/', subscribe, name='subscribe'),
    path('unsubscribe/<int:pk>/', unsubscribe, name='unsubscribe'),
    path('categories/', get_category, name='category_all'),
    path('check/', IndexView.as_view()),

]
