from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import CustomUserCreationForm


class CustomLogoutView(LogoutView):
    template_name = 'users/logout.html'
    next_page = reverse_lazy('users:logout')

class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('catalog:product_list')
