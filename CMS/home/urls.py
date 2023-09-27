from django.urls import path
from . import views

urlpatterns = [
    path('', views.articleList, name='index'),
    path('register/', views.sign_up, name='register'),
    path('user/<int:pk>/', views.showUserDetail, name='user'),
    path('userUpdate/<int:pk>/', views.updateUser, name='userUpdate'),
    path('article/<int:pk>/', views.articleDetail, name='article'),
    path('like/<int:pk>/', views.likeArticle, name='likeArticle'),
    path('rate/<int:post_id>/<int:rating>/', views.rateArticle, name='rateArticle'),
]

