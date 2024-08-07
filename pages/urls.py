from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('privacy/', views.privacy, name='privacy'),
    path('article/', views.article, name='article'),
    path('article/<int:inter_id>/', views.articleDetail, name='article-detail'),
]