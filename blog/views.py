from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from config import settings
from .models import Blog


class BlogListView(ListView):
    model = Blog
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_published=True)


class BlogDetailView(LoginRequiredMixin, DetailView):
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
            recipient_list = ['hrustam911@mail.ru']
            try:
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                print(f"Письмо успешно отправлено от {from_email} получателям: {', '.join(recipient_list)}")
            except Exception as e:
                print(f"Ошибка при отправке письма: {e}")

        return self.object



class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['title', 'content', 'preview', 'is_published', 'views_counter', 'author_email']
    success_url = reverse_lazy('blog:blog_list')


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ['title', 'content', 'preview', 'is_published', 'views_counter']
    success_url = reverse_lazy('blog:blog_list')

    def get_success_url(self):
        return reverse_lazy('blog:blog_detail', args=[self.kwargs.get('pk')])

class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blog_list')
