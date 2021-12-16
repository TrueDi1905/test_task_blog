from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('new_post/', views.new_post, name='new_post'),
    path('<str:username>/', views.blog, name='blog'),
    path('<str:username>/follow/', views.blog_follow, name='follow'),
    path('<str:username>/unfollow/', views.blog_unfollow, name='unfollow'),
    path('<int:id>/read/', views.read_post, name='read'),
    path('', views.index, name='news'),
    ]
