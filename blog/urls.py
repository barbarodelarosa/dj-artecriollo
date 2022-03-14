from django.urls import path

from . import views

app_name='blog'
urlpatterns = [
   
    path('', views.IndexBlogView.as_view(), name='posts'),
    path('tags/', views.TagsBlogView.as_view(), name='tags-list'),
    path('tags/<slug>/', views.TagDetailView.as_view(), name='tag-detail'),
    path('posts/', views.PostsListView.as_view(), name='posts'),
    path('<slug>/', views.CategoryDetailView.as_view(), name='category'),
    path('<category>/<slug>/', views.PostDetailView.as_view(), name='post-detail'),




]





