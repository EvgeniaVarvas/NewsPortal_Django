from django.urls import path
from .views import ArticleList, CreateNews, NewsList, PostDetail, PostUpdate, PostDelete, PostSearch


urlpatterns = [
    path('common_list/news/', NewsList.as_view(), name='news_list'),
    path('common_list/article/', ArticleList.as_view(), name='article_list'),
    path('common_list/create_news/', CreateNews.as_view(), name='create_news'),
    path('common_list/post_detail/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('common_list/create_news/<int:pk>/', PostUpdate.as_view(), name='post_update'),
    path('common_list/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('post_search/', PostSearch.as_view(), name='post_search'),
    
]