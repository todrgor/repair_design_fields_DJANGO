from django.shortcuts import render, redirect
# from django.core.exceptions import ObjectDoesNotExist

from django.views.generic.list import ListView

from django.contrib.auth import logout, login
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, UpdateView
from django.core.files.storage import FileSystemStorage


from authapp.forms import RegisterForm, LoginForm
from authapp.models import *
from publicationapp.models import *
from .forms import *


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
    context_object_name = 'opened_user'
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

def UpdateAccount(request, pk):
    edited_user = User.objects.get(id=pk)
    form_user = UserForm({'username': edited_user.username, 'photo': edited_user.photo.url, 'role': edited_user.role, 'bio': edited_user.bio, 'age': edited_user.age, 'phone_number': edited_user.phone_number, })
    if edited_user.role.id == 2:
        edited_user_expert_info = ExpertInfo.objects.filter(expert_id=pk)
        if edited_user_expert_info:
            edited_user_expert_info = ExpertInfo.objects.get(expert_id=pk)
        else:
            edited_user_expert_info = ExpertInfo.objects.create(expert_id=edited_user)
            edited_user_expert_info.save()
        form_user_expert = UserExpertForm({'knowledge': edited_user_expert_info.knowledge, 'offer': edited_user_expert_info.offer, 'site': edited_user_expert_info.site, 'address': edited_user_expert_info.address, 'telegram': edited_user_expert_info.telegram, 'whatsapp': edited_user_expert_info.whatsapp, 'viber': edited_user_expert_info.viber, 'vk': edited_user_expert_info.vk, 'inst': edited_user_expert_info.inst, 'ok': edited_user_expert_info.ok, 'fb': edited_user_expert_info.fb, 'other': edited_user_expert_info.other, })
    else:
        form_user_expert = UserExpertForm()
    edited_user_subs = UserSubscribes.objects.filter(subscriber_id=pk)
    print(edited_user_subs)
    if request.method == 'POST':
        form_user = UserForm(request.POST)
        edited_user_post = request.POST
        if request.FILES['photo']:
            edited_user.__dict__.update({'username': edited_user_post['username'], 'photo': ('users_avatars/' + str(request.FILES['photo'])), 'bio': edited_user_post['bio'], 'age': edited_user_post['age'], 'phone_number': edited_user_post['phone_number'], })
            fs = FileSystemStorage()
            photo_file = fs.save(('users_avatars/' + request.FILES['photo'].name), request.FILES['photo'])
        else:
            edited_user.__dict__.update({'username': edited_user_post['username'], 'bio': edited_user_post['bio'], 'age': edited_user_post['age'], 'phone_number': edited_user_post['phone_number'], })
        edited_user.save()
        if edited_user.role.id == 2:
            edited_user_expert_info.__dict__.update({'knowledge': edited_user_post['knowledge'], 'offer': edited_user_post['offer'], 'site': edited_user_post['site'], 'address': edited_user_post['address'], 'telegram': edited_user_post['telegram'], 'whatsapp': edited_user_post['whatsapp'], 'viber': edited_user_post['viber'], 'vk': edited_user_post['vk'], 'inst': edited_user_post['inst'], 'ok': edited_user_post['ok'], 'fb': edited_user_post['fb'], 'other': edited_user_post['other'], })
            edited_user_expert_info.save()
        return redirect('auth:account_one', pk=edited_user.id)

    title = 'Настройки пользователя ' + edited_user.username
    return render(request, 'authapp/create_new_or_update.html', {'title': title, 'form_user': form_user, 'form_user_expert': form_user_expert, 'edited_user': edited_user, 'edited_user_subs': edited_user_subs, })
