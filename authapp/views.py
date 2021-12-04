from django.shortcuts import render, redirect

from django.views.generic.list import ListView

from django.contrib.auth import logout, login
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, UpdateView

from authapp.forms import RegisterForm, LoginForm
from authapp.models import *
from publicationapp.models import *

# def login(request):
#     pass
#
# def logout(request):
#     pass


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


class AccountOneWatch(ListView):
    model = User
    template_name = 'authapp/user_one.html'
    context_object_name = 'user'
    allow_empty = False # сделать ответ на случай, если публикации с введённым id не существует

    def get_queryset(self):
        return User.objects.get(id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(AccountOneWatch, self).get_context_data(**kwargs)
        user_role = User.objects.get(id=self.kwargs['pk']).role.id

        if user_role == 2 or user_role == 4:
            try:
                expert_info = ExpertInfo.objects.get(expert_id=self.kwargs['pk'])
                if expert_info.knowledge or expert_info.site or expert_info.site or expert_info.address or expert_info.whatsapp or expert_info.viber or expert_info.vk or expert_info.inst or expert_info.ok or expert_info.fb or expert_info.other:
                    expert_info = expert_info
                else:
                    expert_info = None

            except ObjectDoesNotExist:
                expert_info = None
            except MultipleObjectsReturned:
                expert_info = None

            expert_pubs = Publication.objects.filter(author=self.kwargs['pk'])
            pub_has_tags = PubHasTags.objects.filter(pub_id__in=expert_pubs)
        else:
            expert_info = None
            expert_pubs = None
            pub_has_tags = None

        context.update({
            'expert_info': expert_info,
            'expert_pubs': expert_pubs,
            'pub_has_tags': pub_has_tags,
        })
        return context
