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
    def get_context_data(self, **kwargs):
        

        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
 
        return context

    

class TagsBlogView(generic.ListView):
    model = Tag
    template_name='blog/blog_tags_list.html'
    ordering=['name']
    def get_context_data(self, **kwargs):
        

        context = super(TagsBlogView, self).get_context_data(**kwargs)
        
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
 
        return context


class TagDetailView(generic.DetailView):
    model = Tag
    template_name='blog/tag_detail.html'
    def get_context_data(self, **kwargs):
        

        context = super(TagDetailView, self).get_context_data(**kwargs)
        
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
 
        return context



class PostsListView(generic.ListView):
    model = Post
    template_name='blog/posts_list.html'
    ordering=['-updated_at', '-created_at']
    
    def get_context_data(self, **kwargs):
        

        context = super(PostsListView, self).get_context_data(**kwargs)
        
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
 
        return context


class PostDetailView(generic.DetailView):
    model = Post
    template_name='blog/post_detail.html'
    

    def get_context_data(self, **kwargs):
        

        context = super(PostDetailView, self).get_context_data(**kwargs)
        
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
 
        return context


