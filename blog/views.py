from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from config import settings
from .models import Blog


class BlogListView(ListView):
    model = Blog
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_published=True)


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()


        if self.object.views_counter == 100:
            subject = f'Поздравляем! Ваша статья "{self.object.title}" достигла 100 просмотров!'
            message = (
                f'Привет!\n\n'
                f'Мы рады сообщить, что ваша статья "{self.object.title}" ')
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [self.object.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        return self.object



class BlogCreateView(CreateView):
    model = Blog
    fields = ['title', 'content', 'preview', 'is_published', 'views_counter']
    success_url = reverse_lazy('blog:blog_list')


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ['title', 'content', 'preview', 'is_published', 'views_counter']
    success_url = reverse_lazy('blog:blog_list')

    def get_success_url(self):
        return reverse_lazy('blog:blog_detail', args=[self.kwargs.get('pk')])

class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blog_list')
