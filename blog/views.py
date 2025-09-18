from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from .models import Blog


class BlogListView(ListView):
    model = Blog
    paginate_by = 3


class BlogDetailView(DetailView):
    model = Blog


class BlogCreateView(CreateView):
    model = Blog
    fields = ['title', 'content', 'preview', 'is_published', 'views_counter']
    success_url = reverse_lazy('blog:blog_list')


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ['title', 'content', 'preview', 'is_published', 'views_counter']
    success_url = reverse_lazy('blog:blog_list')


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blog_list')
