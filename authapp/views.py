from django.shortcuts import render, redirect

from django.contrib.auth import logout, login
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, UpdateView

from authapp.forms import RegisterForm, LoginForm
from authapp.models import User

def login(request):
    pass

def logout(request):
    pass


class UserLoginView(LoginView):
    template_name = "authapp/login.html"
    model = User
    title ='Вход в ИС'
    success_url = reverse_lazy('main')
    form_class = LoginForm

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('main')


class UserRegisterView(TemplateView):
    template_name = "authapp/register.html"

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = RegisterForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('auth:login'))
        else:
            form = RegisterForm()

        content = {
            'title': 'Регистрация',
            'form': form
        }

        return render(request, self.template_name, content)
