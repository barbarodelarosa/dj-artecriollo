from django.shortcuts import render
from django.views import generic
from requests import models
from .models import Category, Tag, Post
# Create your views here.

class IndexBlogView(generic.ListView):
    model=Category
    # models = Category
    template_name='blog/index_blog_category_list.html'
    ordering=['name']

class CategoryDetailView(generic.DetailView):
    model = Category
    template_name='blog/category_detail.html'
    

class TagsBlogView(generic.ListView):
    model = Tag
    template_name='blog/blog_tags_list.html'
    ordering=['name']

class TagDetailView(generic.DetailView):
    model = Tag
    template_name='blog/tag_detail.html'


class PostsListView(generic.ListView):
    model = Post
    template_name='blog/blog_posts_list.html'
    ordering=['updated_at', 'created_at']

class PostDetailView(generic.DetailView):
    model = Post
    template_name='blog/post_detail.html'