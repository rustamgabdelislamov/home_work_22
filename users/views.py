from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView
import os
from dotenv import load_dotenv
from users.forms import CustomUserCreationForm
from users.models import CustomUser

load_dotenv()

def logout_view(request):
    logout(request)
    return redirect("/")

# class CustomLogoutView(LogoutView):
#     template_name = 'users/logout.html'
#     # def get_redirect_url(self):
#     #     """Переопределяем, чтобы URL вычислялся при запросе."""
#     #     return reverse('users:logout')

class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('catalog:product_list')


    # def form_valid(self, form):
    #     user = form.save()
    #     self.send_welcome_email(user.email)
    #     return super().form_valid(form)


    # def send_welcome_email(self, user_email):
    #     subject = 'Добро пожаловать в наш сервис!'
    #     message = 'Спасибо что зарегистрировались в нашем сервисе'
    #     from_email = os.getenv('EMAIL_HOST_USER')
    #     recipient_list = [user_email]
    #     send_mail(subject, message, from_email, recipient_list)


class UsersListView(ListView):
    model = CustomUser
    context_object_name = 'customusers_list'
    template_name = 'users/customusers_list.html'


