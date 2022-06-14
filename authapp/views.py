
from django.db.models import Q
# from django.db.models.functions import Lower

from django.shortcuts import render, redirect

from django.views.generic.list import ListView
from django.views.generic import TemplateView, UpdateView

from django.contrib.auth import logout, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, HttpResponseNotFound, Http404
from django.urls import reverse, reverse_lazy

from authapp.forms import RegisterForm, LoginForm
from .forms import *
from authapp.models import *
from publicationapp.models import *
from django.utils import timezone

from phonenumber_field.phonenumber import PhoneNumber

#   очистить ссылку от домена
def url_without_domen(url):
    domens_list = (
        'ru',
        'com',
        'me'
    )
    for domen in domens_list:
        if ('.'+ domen +'/') in url and url.find('.') == url.find('.'+ domen +'/'):
            url = url[(url.find('.') +len(domen) +2):]
    return url

    # #   получить всю сссылку
    # def full_url(url, direct_to):
    #     directions_list = {
    #         'tg': 't.me/',
    #         'wa': 'wa.me/',
    #         'vb': 'vb.me/',
    #         'lol': 'life-online.ru/',
    #         'vk': 'vk.com/',
    #         'ig': 'instagram.com/',
    #         'tw': 'twitter.com/',
    #         'ok': 'ok.ru/',
    #     }
    #     url = directions_list[direct_to] + url.url_without_domen(url_without_protocol(url.url_without_pre_domen(url))) if direct_to in directions_list else ''
    #     return url

#   очистить ссылку от протокола и тега
def url_without_protocol(url):
    remove_slugs_list = (
        '@',
        'https://',
        'http://',
        'www.'
        )
    for slug in remove_slugs_list:
        if slug in url and url.find(slug) == 0:
            url = url[len(slug):]
    return url



#   включение-отключение получение уведомлений от автора
def toggle_get_noti_from_author(request, pk):
    if request.is_ajax():
        if request.user.is_authenticated:
            duplicate = request.user.following_for.filter(id=pk)
            star = User.objects.get(id=pk)

            if not duplicate:
                if request.user != star:
                    request.user.following_for.add(star)
                    result = 1

                    Notifications.objects.create(
                        type = ActionTypes.objects.get(id=3030200),
                        preview = request.user.photo.name,
                        content = 'Пользователь «'+ request.user.username +'» подписался на уведомления о Ваших новых публикациях.',
                        hover_text = 'Теперь у Вас ' + str( User.objects.filter(following_for__id=star.id).count() ) + ' подписчиков.'
                    ).receiver.add(star)

                    Notifications.objects.create(
                        type = ActionTypes.objects.get(id=3030200),
                        preview = star.photo.name,
                        content = 'Теперь вы будете получать уведомления о новых публикациях пользователя «'+ User.objects.get(id=pk).username +'»',
                        hover_text = 'Теперь у Вас ' + str( request.user.following_for.count() ) + ' источников уведомлений о новых публикациях',
                        url = reverse('auth:one', args=(star.id,)),
                        url_text = 'Открыть пользователя'
                    ).receiver.add(request.user)

                    JournalActions.objects.create(
                        type = ActionTypes.objects.get(id=3030200),
                        action_person = request.user,
                        action_content = 'Подписка на пользователя «'+ star.username +'» пользователем «'+ request.user.username +'».',
                        action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')], [user_star «'+ star.username +'» (id: '+ str(star.id) +')]'
                    )
                else:
                    result = 0
                    Notifications.objects.create(
                        type = ActionTypes.objects.get(id=3030400),
                        preview = request.user.photo.name,
                        content = 'Вы пытались подписаться сами на себя. Давайте так не делать :)',
                        hover_text = 'Не ну а шо вы в самый раз'
                    ).receiver.add(request.user)

                    JournalActions.objects.create(
                        type = ActionTypes.objects.get(id=3030200),
                        action_person = request.user,
                        action_content = 'Попытка подписки на самого себя пользователем «'+ request.user.username +'».',
                        action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')]'
                    )
            else:
                request.user.following_for.remove(star)
                duplicate.delete()
                result = 0

                JournalActions.objects.create(
                    type = ActionTypes.objects.get(id=3030500),
                    action_person = request.user,
                    action_content = 'Отписка на пользователя «'+ star.username +'» пользователем «'+ request.user.username +'».',
                    action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')], [user_star «'+ star.username +'» (id: '+ str(star.id) +')]'
                )

            return JsonResponse({'result': result})


#   получение сигнала о том,
#   что новые уведомления открыты и прочитаны
def new_noti_were_seen(request, pk):
    #   переписать через property юзера
    if request.is_ajax():
        new_noties = Notifications.objects.filter(receiver=request.user).exclude(receiver_saw=request.user)
        if new_noties:
            result = 1
            for nn in new_noties:
                nn.receiver_saw.add(request.user)
                nn.save()
        else:
            result = 0
        return JsonResponse({'result': result})


#   регистрация пользователя
class UserRegisterView(TemplateView):
    template_name = "authapp/register.html"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('main'))
        else:
            return 1

    def dispatch(self, request, *args, **kwargs):
        form = RegisterForm()
        if request.method == 'POST':
            form = RegisterForm(request.POST, request.FILES)
            if form.is_valid():
                registered_user = form.save()

                JournalActions.objects.create(
                    type = ActionTypes.objects.get(id=3010300),
                    action_person = registered_user,
                    action_content = 'Зарегистрировался пользователь «'+ registered_user.username +'».',
                    action_subjects_list = '[user «'+ registered_user.username +'». (id: '+ str(registered_user.id) +')]'
                )

                return HttpResponseRedirect(reverse('login'))

        content = {
            'title': 'Регистрация',
            'form': form,
        }
        return render(request, self.template_name, content)


#   авторизация пользователя
class UserLoginView(LoginView):
    template_name = "authapp/login.html"
    model = User
    title ='Авторизация'
    success_url = reverse_lazy('main')
    form_class = LoginForm

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return redirect('main')
        else:
            return 1

    def form_valid(self, form):
        login(self.request, form.get_user())

        JournalActions.objects.create(
            type = ActionTypes.objects.get(id=3010200),
            action_person = self.request.user,
            action_content = 'Авторизовался пользователь «'+ self.request.user.username +'».',
            action_subjects_list = '[user «'+ self.request.user.username +'». (id: '+ str(self.request.user.id) +')]'
        )
        return HttpResponseRedirect(self.get_success_url())


#   выход из учётной записи пользователя
def UserLogout(request):
    JournalActions.objects.create(
        type = ActionTypes.objects.get(id=3010100),
        action_person = request.user,
        action_content = 'Вышел из аккаунта пользователь «'+ request.user.username +'».',
        action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')]'
    )
    logout(request)
    return redirect('main')



#   просмотр одной странички пользователя
class AccountOneWatch(ListView):
    model = User
    template_name = 'authapp/user_one.html'

    def get_context_data(self, **kwargs):
        context = super(AccountOneWatch, self).get_context_data(**kwargs)
        opened_user = expert_info = expert_pubs = saved_pubs = None

        if User.objects.filter(id=self.kwargs['pk']):
            opened_user = User.objects.get(id=self.kwargs['pk'])
            opened_user.seen_count +=1
            opened_user.save()

            if self.request.user.is_authenticated:
                JournalActions.objects.create(
                    type = ActionTypes.objects.get(id=4010200),
                    action_person = self.request.user,
                    action_content = 'Просмотрена страница пользователя «'+ opened_user.username +'» пользователем «'+ self.request.user.username +'».',
                    action_subjects_list = '[user «'+ self.request.user.username +'». (id: '+ str(self.request.user.id) +')], [opened_user «'+ opened_user.username +'». (id: '+ str(opened_user.id) +')]'
                )

            saved_pubs = [sp.pub.id for sp in SavedPubs.objects.filter(saver=self.request.user)] if self.request.user.is_authenticated else None

            if opened_user.role.id in [2, 4]:
                expert_pubs = Publication.objects.filter(author=self.kwargs['pk'], type__id__in=[11, 21, 31])
                try:
                    expert_info = ExpertInfo.objects.get(expert_account=self.kwargs['pk'])
                except ObjectDoesNotExist:
                    expert_info = None
        else:
            if self.request.user.is_authenticated:
                JournalActions.objects.create(
                    type = ActionTypes.objects.get(id=4010404),
                    action_person = self.request.user,
                    action_content = 'Попытка просмотра страницы несуществующего пользователя пользователем «'+ self.request.user.username +'».',
                    action_subjects_list = '[user «'+ self.request.user.username +'». (id: '+ str(self.request.user.id) +')], [doesnt_exist_user_id: '+ str(self.kwargs['pk']) +')]'
                )

        context.update({
            'opened_user': opened_user,
            'expert_info': expert_info,
            'expert_pubs': expert_pubs,
            'saved_pubs': saved_pubs,
        })
        return context


#   создание учётной записи пользователя суперадмином
def CreateAccount(request):
    if not request.user.is_authenticated:
        return redirect('main')
    if not request.user.role.id == 4:
        return redirect('main')

    edited_user = None
    form_user = UserForm()
    form_expert_user = UserExpertForm()
    form_user_password = UserPasswordForm()

    if request.method == 'POST':
        form_user = UserForm(request.POST)
        form_expert_user = UserExpertForm(request.POST)
        form_user_password = UserPasswordForm(request.POST)

        if User.objects.filter(username=request.POST['username']):
            form_user.add_error('username', 'Пользователь с таким никнеймом уже существует. Пожалуйста, введите иное.')

        if User.objects.filter(phone_number=request.POST['phone_number']):
            form_user.add_error('phone_number', 'Пользователь с таким номером телефона уже существует. Пожалуйста, введите иной.')

        if 'role' in request.POST and not request.POST['role']:
            form_user.add_error('role', 'Некорректно заполнено поле. Пожалуйста, заполните его правильно.')

        if form_user.is_valid():
            method_POST = request.POST
            edited_user = User.objects.create(
                username=method_POST['username'],
                bio=method_POST['bio'],
                age=method_POST['age'],
                phone_number=method_POST['phone_number'],
                role=UserRoles.objects.get(id=method_POST['role'])
                )
            edited_user.set_password(method_POST['password'])

            if 'photo' in request.FILES:
                edited_user.__dict__.update({
                    'photo': ('users_avatars/' + str(request.FILES['photo'])),
                    })
                fs = FileSystemStorage()
                photo_file = fs.save(('users_avatars/' + request.FILES['photo'].name), request.FILES['photo'])

            edited_user.save()
            if method_POST['role'] in [2, '2', 4, '4']:
                edited_user_expert_info = ExpertInfo.objects.filter(expert_account=edited_user.id)
                edited_user_expert_info = ExpertInfo.objects.get(expert_account=edited_user.id) if edited_user_expert_info else ExpertInfo.objects.create(expert_account=edited_user)
                edited_user_expert_info.__dict__.update({
                    'knowledge':                                                   method_POST['knowledge'],
                    'offer':                                                       method_POST['offer'],
                    'bisness_phone_number':                                        method_POST['bisness_phone_number'],
                    'site':                                   url_without_protocol(method_POST['site']),
                    'address':                                                     method_POST['address'],
                    'telegram':             url_without_domen(url_without_protocol(method_POST['telegram'])),
                    'whatsapp':             url_without_domen(url_without_protocol(method_POST['whatsapp'])),
                    'viber':                url_without_domen(url_without_protocol(method_POST['viber'])),
                    'lol':                  url_without_domen(url_without_protocol(method_POST['lol'])),
                    'vk':                   url_without_domen(url_without_protocol(method_POST['vk'])),
                    'inst':                 url_without_domen(url_without_protocol(method_POST['inst'])),
                    'ok':                   url_without_domen(url_without_protocol(method_POST['ok'])),
                    'twitter':              url_without_domen(url_without_protocol(method_POST['twitter'])),
                    'other':                                                       method_POST['other'],
                    })
                edited_user_expert_info.save()

            Notifications.objects.create(
                type = ActionTypes.objects.get(id=9910200),
                preview = edited_user.photo.name,
                content = 'Успешно создан аккаунт пользователя «'+ edited_user.username +'»!',
                hover_text = 'Вы большой молодец, что расширяете нам базу пользователей',
                url = reverse('auth:one', args=(edited_user.id,)),
                url_text = 'Открыть пользователя'
            ).receiver.add(request.user)

            JournalActions.objects.create(
                type = ActionTypes.objects.get(id=9910200),
                action_person = request.user,
                action_content = 'Создание аккаунта пользователя «'+ edited_user.username +'» пользователем «'+ request.user.username +'».',
                action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')], [created_user «'+ edited_user.username +'» (id: '+ str(edited_user.id) +')]'
            )

            return redirect('auth:one', pk=edited_user.id)

    title = 'Создать нового пользователя'
    context = {
        'title': title,
        'form_user': form_user,
        'form_expert_user': form_expert_user,
        'form_user_password': form_user_password,
        'edited_user': edited_user,
    }
    return render(request, 'authapp/create_new_account.html', context)


#   изменение учётной записи пользователя
def UpdateAccount(request, pk):
    if not request.user.is_authenticated:
        return redirect('main')
    if not (request.user.role.id == 4 or request.user.id == int(pk)):
        return redirect('main')

    edited_user = User.objects.get(id=pk)
    form_user = UserForm({
        'username': edited_user.username,
        'photo': edited_user.photo.url,
        'role': edited_user.role,
        'bio': edited_user.bio,
        'age': edited_user.age,
        'phone_number': edited_user.phone_number,
        })
    form_expert_user = UserExpertForm()

    if edited_user.role.id in [2, 4]:
        edited_user_expert_info = ExpertInfo.objects.get(expert_account=pk) if ExpertInfo.objects.filter(expert_account=pk) else ExpertInfo.objects.create(expert_account=edited_user).save()
        form_expert_user = UserExpertForm({
            'knowledge': edited_user_expert_info.knowledge,
            'offer': edited_user_expert_info.offer,
            'bisness_phone_number': edited_user_expert_info.bisness_phone_number,
            'site': edited_user_expert_info.site,
            'address': edited_user_expert_info.address,
            'telegram': edited_user_expert_info.telegram,
            'whatsapp': edited_user_expert_info.whatsapp,
            'viber': edited_user_expert_info.viber,
            'lol': edited_user_expert_info.lol,
            'vk': edited_user_expert_info.vk,
            'inst': edited_user_expert_info.inst,
            'ok': edited_user_expert_info.ok,
            'twitter': edited_user_expert_info.twitter,
            'other': edited_user_expert_info.other,
            })

    if request.method == 'POST':
        form_user = UserForm(request.POST)
        form_expert_user = UserExpertForm(request.POST)

        if User.objects.filter(phone_number=request.POST['username']).exclude(id=pk):
            form_user.add_error('username', 'Пользователь с таким никнеймом уже существует. Пожалуйста, введите иное.')

        if User.objects.filter(phone_number=request.POST['phone_number']).exclude(id=pk):
            form_user.add_error('phone_number', 'Пользователь с таким номером телефона уже существует. Пожалуйста, введите иной.')

        if 'role' in request.POST and not request.POST['role']:
            form_user.add_error('role', 'Некорректно заполнено поле. Пожалуйста, заполните его правильно.')

        if form_user.is_valid() and form_expert_user.is_valid():
            method_POST = request.POST
            edited_user.__dict__.update({
                'username': method_POST['username'],
                'bio': method_POST['bio'],
                'age': method_POST['age'],
                'phone_number': method_POST['phone_number'],
                })

            if 'delete_avatar' in method_POST and not 'photo' in request.FILES:
                setattr(edited_user, "photo", User._meta.get_field('photo').get_default())

            if 'photo' in request.FILES:
                edited_user.__dict__.update({
                    'photo': ('users_avatars/' + str(request.FILES['photo'])),
                    })
                fs = FileSystemStorage()
                photo_file = fs.save(('users_avatars/' + request.FILES['photo'].name), request.FILES['photo'])

            if (edited_user.role.id in [2, 4]) or ('role' in method_POST and request.user.role.id == 4):
                if 'role' in method_POST:
                    if method_POST['role'] == "4" and User.objects.filter(role=UserRoles.objects.get(id=4)).count() > 1:
                        edited_user.role = edited_user.role
                    else:
                        edited_user.role = UserRoles.objects.get(id=method_POST['role'])

                edited_user_expert_info = ExpertInfo.objects.get(expert_account=pk) if ExpertInfo.objects.filter(expert_account=pk) else ExpertInfo.objects.create(expert_account=edited_user)

                edited_user_expert_info.knowledge =                                                   method_POST['knowledge']             if method_POST['knowledge']            else ''
                edited_user_expert_info.offer =                                                       method_POST['offer']                 if method_POST['offer']                else ''
                edited_user_expert_info.site =                                   url_without_protocol(method_POST['site'])                 if method_POST['site']                 else ''
                edited_user_expert_info.bisness_phone_number =                                        method_POST['bisness_phone_number']  if method_POST['bisness_phone_number'] else ''
                edited_user_expert_info.address =                                                     method_POST['address']               if method_POST['address']              else ''
                edited_user_expert_info.telegram =             url_without_domen(url_without_protocol(method_POST['telegram']))            if method_POST['telegram']             else ''
                edited_user_expert_info.whatsapp =             url_without_domen(url_without_protocol(method_POST['whatsapp']))            if method_POST['whatsapp']             else ''
                edited_user_expert_info.viber =                url_without_domen(url_without_protocol(method_POST['viber']))               if method_POST['viber']                else ''
                edited_user_expert_info.lol =                  url_without_domen(url_without_protocol(method_POST['lol'] ))                if method_POST['lol']                  else ''
                edited_user_expert_info.vk =                   url_without_domen(url_without_protocol(method_POST['vk'] ))                 if method_POST['vk']                   else ''
                edited_user_expert_info.inst =                 url_without_domen(url_without_protocol(method_POST['inst']))                if method_POST['inst']                 else ''
                edited_user_expert_info.ok =                   url_without_domen(url_without_protocol(method_POST['ok']))                  if method_POST['ok']                   else ''
                edited_user_expert_info.twitter =              url_without_domen(url_without_protocol(method_POST['twitter']))             if method_POST['twitter']              else ''
                edited_user_expert_info.other =                                                       method_POST['other']                 if method_POST['other']                else ''
                edited_user_expert_info.save()

            edited_user.save()

            if request.user.id == edited_user.id:
                Notifications.objects.create(
                    type = ActionTypes.objects.get(id=3010201),
                    content = 'Аккаунт успешно отредактирован.',
                    hover_text = 'Вы большой молодец'
                ).receiver.add(request.user)

                JournalActions.objects.create(
                    type = ActionTypes.objects.get(id=3010201),
                    action_person = request.user,
                    action_content = 'Изменил свой аккаунт пользователь «'+ request.user.username +'».',
                    action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')]'
                )

            else:
                Notifications.objects.create(
                    type = ActionTypes.objects.get(id=9910201),
                    preview = edited_user.photo.name,
                    content = 'Успешно отредактирован аккаунт пользователя «'+ edited_user.username +'»!',
                    hover_text = 'Вы большой молодец',
                    url = reverse('auth:one', args=(edited_user.id,)),
                    url_text = 'Открыть пользователя'
                ).receiver.add(request.user)

                Notifications.objects.create(
                    type = ActionTypes.objects.get(id=9910201),
                    content = 'Ваш аккаунт отредактирован суперпользователем «'+ request.user.username +'»!',
                    hover_text = 'Вы большой молодец'
                ).receiver.add(edited_user)

                JournalActions.objects.create(
                    type = ActionTypes.objects.get(id=9910201),
                    action_person = request.user,
                    action_content = 'Изменение аккаунта пользователя «'+ edited_user.username +'» пользователем «'+ request.user.username +'».',
                    action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')], [edited_user «'+ edited_user.username +'» (id: '+ str(edited_user.id) +')]'
                )

            return redirect('auth:one', pk=edited_user.id)

    title = 'Настройки пользователя' if request.user.id == int(pk) else 'Настройки пользователя «' + edited_user.username +'»'
    context = {
        'title': title,
        'form_user': form_user,
        'form_expert_user': form_expert_user,
        'edited_user': edited_user,
    }
    return render(request, 'authapp/update_account.html', context)


#   изменение пароля
def ChangePassword(request, pk):
    if not request.user.is_authenticated:
        return redirect('main')
    if request.user.role.id != 4 and request.user.id != pk:
        return redirect('main')

    edited_user = User.objects.get(id=pk)
    form = PasswordChangeForm(edited_user) if request.user.id == pk else UserPasswordForm()
    if request.method == 'POST':
        print(request.POST)
        form = PasswordChangeForm(edited_user, request.POST) if request.user.id == pk else UserPasswordForm(request.POST)
        if form.is_valid():
            if request.user.id == pk:
                form = form.save()
                update_session_auth_hash(request, form)

                Notifications.objects.create(
                    type = ActionTypes.objects.get(id=3010202),
                    content = 'Успешно изменён пароль! Запишите его себе: «' + request.POST['new_password1'] +'». И не забывайте :)',
                    hover_text = 'Вы молодец, что заботетесь о своей безопасности! С заботой, «Ремонт и Дизайн» ❤'
                ).receiver.add(edited_user)

                JournalActions.objects.create(
                    type = ActionTypes.objects.get(id=3010202),
                    action_person = request.user,
                    action_content = 'Смена своего пароля пользователем «'+ request.user.username +'».',
                    action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')]'
                )
            else:
                password = request.POST['password']
                edited_user.set_password(password)
                edited_user.save()

                Notifications.objects.create(
                    type = ActionTypes.objects.get(id=9910202),
                    content = 'Успешно изменён пароль пользователя «' + edited_user.username +'»! Теперь он такой: «' + password +'».',
                    hover_text = 'зачем правда ну ладно',
                    url = reverse('auth:one', args=(edited_user.id,)),
                    url_text = 'Открыть пользователя'
                ).receiver.add(request.user)

                Notifications.objects.create(
                    type = ActionTypes.objects.get(id=9910202),
                    content = 'Ваш пароль был изменён администратором. Запишите его себе: «' + password +'». И не забывайте :)',
                    hover_text = 'С заботой, «Ремонт и Дизайн» ❤'
                ).receiver.add(edited_user)

                JournalActions.objects.create(
                    type = ActionTypes.objects.get(id=9910202),
                    action_person = request.user,
                    action_content = 'Смена пароля пользователя «'+ edited_user.username +'» пользователем «'+ request.user.username +'».',
                    action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')], [edited_user «'+ edited_user.username +'» (id: '+ str(edited_user.id) +')]'
                )
            return redirect('auth:settings', pk=pk)

    title = 'Смена пароля' if request.user == edited_user else 'Смена пароля пользователя «' + edited_user.username +'»'
    context = {
        'title': title,
        'form': form,
        'edited_user': edited_user,
    }
    return render(request, 'authapp/change_password.html', context)


#   удаление учётной записи пользователя
def DeleteAccount(request, pk):
    if request.user.is_authenticated:
        user = User.objects.get(id=pk)

        if (request.user.id == user.id and not user.is_only_one_superuser) or (request.user.role.id == 4 and user.role.id != 4):
            user_id = user.id
            user_name = user.username
            user_photo = user.photo.name
            user.delete()

            if request.user.id != user_id:
                Notifications.objects.create(
                    type = ActionTypes.objects.get(id=9910500),
                    preview = user_photo,
                    content = 'Успешно удалён пользователь «' + user_name +'»',
                    hover_text = 'Вот и зачем Вы его так?',
                    url = reverse('admin_mine:user_create_new'),
                    url_text = 'Создать нового'
                ).receiver.add(request.user)

                JournalActions.objects.create(
                    type = ActionTypes.objects.get(id=9910500),
                    action_person = request.user,
                    action_content = 'Удаление аккаунта пользователя «'+ user_name +'» пользователем «'+ request.user.username +'».',
                    action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')], [deleted_user «'+ user_name +'» (id: '+ str(user_id) +')]'
                )

                return redirect('admin_mine:users')
            else:
                return redirect('logout')


#   подать заявку на аминистратора
def BecomeATeammember(request):
    if not request.user.is_authenticated:
        return HttpResponse("Вы ещё не авторизированы, Вам стоит сначала <a href='/login/'>авторизоваться</a>. <a href='/'>На главную</a>")
    if request.user.role.id == 3:
        return HttpResponse("Вы уже участник нашей команды, Вам не нужно подаввать заявку на свою же роль. Ну вот зачем? <a href='/'>На главную</a>")

    if request.method == 'POST':
        if request.POST['desc']:
            contacting_support = ContactingSupport.objects.create(
                title=('Заявка на роль модератора от пользователя «' + request.user.username +'»'),
                type=ContactingSupportTypes.objects.get(id=22),
                asked_by=request.user,
                ask_content=request.POST['desc'],
                when_asked=timezone.now(),
                ask_additional_info=999
                )

            if request.FILES:
                fs = FileSystemStorage()
                photos = request.FILES.getlist('photos')
                i_count = 0
                for i in photos:
                    fs.save(('contacting_support_media/' + photos[i_count].name), photos[i_count])
                    ContactingSupportPhotos.objects.create(contacting_support_action=contacting_support, photo=('contacting_support_media/' + photos[i_count].name))
                    i_count +=1

            Notifications.objects.create(
                type = ActionTypes.objects.get(id=1014200),
                content = 'Ваша заявка на роль администратора принята на рассмотрение. О нашем решении Вы узнаете через уведомление. Скоро Вы увидите здесь ответ.',
                hover_text = 'Ожидайте ответа!'
            ).receiver.add(request.user)

            JournalActions.objects.create(
                type = ActionTypes.objects.get(id=1014200),
                action_person = request.user,
                action_content = 'Заявка на роль администратора от пользователя «'+ request.user.username +'».',
                action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')], [letter_to_support «'+ contacting_support.title +'» (id: '+ str(contacting_support.id) +')]'
            )
            return redirect('/')

    title = 'Заявка на роль администратора — стать частью команды «Ремонт и Дизайн»'
    form = BecomeATeammemberForm()
    context = {
        'title': title,
        'form': form,
    }
    return render(request, 'authapp/become_a_teammemder.html', context)


#   подать заявку на автора
def BecomeAnAuthor(request):
    if not request.user.is_authenticated:
        return HttpResponse("Вы ещё не авторизированы, Вам стоит сначала <a href='/login/'>авторизоваться</a>. <a href='/'>На главную</a>")
    if request.user.role.id == 2:
        return HttpResponse("Вы уже автор публикаций, Вам не нужно подаввать заявку на свою же роль. Ну вот зачем? <a href='/'>На главную</a>")

    if request.method == 'POST':
        if request.POST['desc']:
            contacting_support = ContactingSupport.objects.create(
                title=('Заявка на роль автора от пользователя «' + request.user.username +'»'),
                type=ContactingSupportTypes.objects.get(id=21),
                asked_by=request.user,
                ask_content=request.POST['desc'],
                ask_additional_info=999,
                when_asked=timezone.now()
                )

            if request.POST['knowledge'] or request.POST['offer'] or request.POST['bisness_phone_number'] or request.POST['site'] or request.POST['address'] or request.POST['telegram'] or request.POST['whatsapp'] or request.POST['viber'] or request.POST['lol'] or request.POST['vk'] or request.POST['inst'] or request.POST['ok'] or request.POST['twitter'] or request.POST['other']:
                becomer_expert_info = ExpertInfo.objects.filter(expert_account=request.user.id)
                if becomer_expert_info:
                    becomer_expert_info = ExpertInfo.objects.get(expert_account=request.user.id)
                else:
                    becomer_expert_info = ExpertInfo.objects.create(expert_account=request.user)

                becomer_expert_info.__dict__.update({
                    'knowledge':                                                   request.POST['knowledge'],
                    'offer':                                                       request.POST['offer'],
                    'site':                                   url_without_protocol(request.POST['site']),
                    'bisness_phone_number':                                        request.POST['bisness_phone_number'],
                    'address':                                                     request.POST['address'],
                    'telegram':             url_without_domen(url_without_protocol(request.POST['telegram'])),
                    'whatsapp':             url_without_domen(url_without_protocol(request.POST['whatsapp'])),
                    'viber':                url_without_domen(url_without_protocol(request.POST['viber'])),
                    'lol':                  url_without_domen(url_without_protocol(request.POST['lol'])),
                    'vk':                   url_without_domen(url_without_protocol(request.POST['vk'])),
                    'inst':                 url_without_domen(url_without_protocol(request.POST['inst'])),
                    'ok':                   url_without_domen(url_without_protocol(request.POST['ok'])),
                    'twitter':              url_without_domen(url_without_protocol(request.POST['twitter'])),
                    'other':                                                       request.POST['other'],
                    })
                becomer_expert_info.save()

            if request.FILES:
                fs = FileSystemStorage()
                photos = request.FILES.getlist('photos')
                i_count = 0
                for i in photos:
                    fs.save(('contacting_support_media/' + photos[i_count].name), photos[i_count])
                    ContactingSupportPhotos.objects.create(contacting_support_action=contacting_support, photo=('contacting_support_media/' + photos[i_count].name))
                    i_count +=1

            Notifications.objects.create(
                type = ActionTypes.objects.get(id=1013200),
                content = 'Ваша заявка стать автором публикаций принята на рассмотрение. О нашем решении Вы узнаете через уведомление. Скоро Вы увидите здесь ответ.',
                hover_text = 'Ожидайте ответа!'
            ).receiver.add(request.user)

            JournalActions.objects.create(
                type = ActionTypes.objects.get(id=1013200),
                action_person = request.user,
                action_content = 'Заявка на роль автора публикаций от пользователя «'+ request.user.username +'».',
                action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')], [letter_to_support «'+ contacting_support.title +'» (id: '+ str(contacting_support.id) +')]'
            )
            return redirect('/')

    title = 'Стать автором публикаций'
    form = BecomeAnAuthorForm()
    expert_info_form = UserExpertForm()
    context = {
        'title': title,
        'form': form,
        'expert_info_form': expert_info_form,
    }
    return render(request, 'authapp/become_an_author.html', context)


#   подать обращение в поддержку: жалоба на пабликацию
#   или пользователя, заявка на автора публикаций
#   или администратора, а также вопрос или идея/предложение
def SendToSupport(request):
    if not request.user.is_authenticated:
        return HttpResponse("Вы ещё не авторизированы, Вам стоит сначала <a href='/login/'>авторизоваться</a>. <a href='/'>На главную</a>")

    if request.method == 'POST':
        if request.POST['desc']:
            # print(str(request.POST))
            if request.POST['desc'].isspace():
                title = 'Обращение в поддержку'
                form = SendToSupportForm({'desc': None, 'type': request.POST['type'],})
                context = {
                    'title': title,
                    'form': form,
                }
                return render(request, 'authapp/send_to_support.html', context)

            ask_additional_info = 0

            if request.POST['type'] == '11':
                pub = Publication.objects.get(id=request.POST['complaint_pub_id'])
                title = 'Жалоба на публикацию «'+ pub.title + '»'
                ask_additional_info = int(request.POST['complaint_pub_id'])
                Notifications.objects.create(
                    type = ActionTypes.objects.get(id=1012200),
                    content = title+ ' принята на рассмотрение. Ожидайте решения. Ответ придёт Вам в виде уведомления.',
                    hover_text = 'Ожидайте ответа! ❤'
                ).receiver.add(request.user)

                Notifications.objects.create(
                    type = ActionTypes.objects.get(id=1012200),
                    content = 'Принята на рассмотрение жалоба на Вашу публикацию «'+ pub.title +'». Ожидайте решения.',
                    hover_text = 'Ожидайте ответа! ❤'
                ).receiver.add(pub.author)

                JournalActions.objects.create(
                    type = ActionTypes.objects.get(id=1012200),
                    action_person = request.user,
                    action_content = 'Жалоба на публикацию «'+ title +'» от пользователя «'+ request.user.username +'».',
                    action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')], [pub_complaint «'+ pub.title +'» (id: '+ str(pub.id) +')]'
                )

            if request.POST['type'] == '12':
                account = User.objects.get(id=request.POST['complaint_account_id'])
                title = 'Жалоба на пользователя «'+ account.username + '»'
                ask_additional_info = int(request.POST['complaint_account_id'])
                Notifications.objects.create(
                    type = ActionTypes.objects.get(id=1011200),
                    content = title+ ' принята на рассмотрение. Ожидайте решения. Ответ придёт Вам в виде уведомления.',
                    hover_text = 'Ожидайте ответа! ❤'
                ).receiver.add(request.user)

                Notifications.objects.create(
                    type = ActionTypes.objects.get(id=1011200),
                    content = 'Принята на рассмотрение жалоба на Ваш аккаунт. Ожидайте решения.',
                    hover_text = 'Ожидайте ответа! ❤'
                ).receiver.add(account)

                JournalActions.objects.create(
                    type = ActionTypes.objects.get(id=1011200),
                    action_person = request.user,
                    action_content = 'Жалоба на пользователя «'+ account.username +'» от пользователя «'+ request.user.username +'».',
                    action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')], [user_complaint «'+ account.username +'» (id: '+ str(account.id) +')]'
                )

            if request.POST['type'] in ['21', '22']:
                if request.user.role.id == 4 and User.objects.filter(role=UserRoles.objects.get(id=4)).count() <= 1:
                    action_type, role_name = 1013200, 'роль автора публикаций' if request.POST['type'] == '21' else 1014200, 'роль администратора'

                    Notifications.objects.create(
                        type = ActionTypes.objects.get(id=action_type),
                        content = 'Ваша заявка на смену роли не может быть принята на рассмотрение. На данный момент в системе всего 1 суперпользователь, поэтому нам опасно менять Вам роль. Найдите наследника и обращайтесь ещё! С заботой, Ваша поддержка «Ремонта и Дизайна»',
                        hover_text = 'По-другому пока не можем. Просим простить нас ❤'
                    ).receiver.add(request.user)

                    JournalActions.objects.create(
                        type = ActionTypes.objects.get(id=action_type),
                        action_person = request.user,
                        action_content = 'Заявка на '+ role_name +' от пользователя «'+ request.user.username +'» (подана '+ str(localize(timezone.now())) +') не обработана – всего 1 суперпользователь в системе.',
                        action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')]'
                    )
                    return redirect('/')

                else:
                    if request.POST['type'] == '21':
                        title = 'Заявка на роль автора от пользователя «'+ request.user.username + '»'
                        Notifications.objects.create(
                            type = ActionTypes.objects.get(id=1013200),
                            content = 'Ваша заявка на роль автора принята на рассмотрение. Ожидайте решения. Ответ придёт Вам в виде уведомления.',
                            hover_text = 'Ожидайте ответа! ❤'
                        ).receiver.add(request.user)

                        JournalActions.objects.create(
                            type = ActionTypes.objects.get(id=1013200),
                            action_person = request.user,
                            action_content = 'Подана заявка на роль автора от пользователя «'+ request.user.username +'».',
                            action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')]'
                        )

                    if request.POST['type'] == '22':
                        title = 'Заявка на роль модератора от пользователя «'+ request.user.username + '»'
                        Notifications.objects.create(
                            type = ActionTypes.objects.get(id=1014200),
                            content = 'Ваша заявка на роль администратора принята на рассмотрение. Ожидайте решения. Ответ придёт Вам в виде уведомления.',
                            hover_text = 'Ожидайте ответа! ❤'
                        ).receiver.add(request.user)

                        JournalActions.objects.create(
                            type = ActionTypes.objects.get(id=1014200),
                            action_person = request.user,
                            action_content = 'Подана заявка на роль администратора от пользователя «'+ request.user.username +'».',
                            action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')]'
                        )

            if request.POST['type'] == '31':
                title = 'Вопрос от пользователя «'+ request.user.username + '»'
                Notifications.objects.create(
                    type = ActionTypes.objects.get(id=1010200),
                    content = 'Ваш вопрос принят. Ожидайте решения. Ответ придёт Вам в виде уведомления.',
                    hover_text = 'Ожидайте ответа! ❤'
                ).receiver.add(request.user)

                JournalActions.objects.create(
                    type = ActionTypes.objects.get(id=1010200),
                    action_person = request.user,
                    action_content = 'Подан вопрос от пользователя «'+ request.user.username +'».',
                    action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')]'
                )

            if request.POST['type'] == '32':
                title = 'Идея и/или предложение от пользователя «'+ request.user.username + '»'
                Notifications.objects.create(
                    type = ActionTypes.objects.get(id=1010200),
                    content = 'Ваша идея и/или предложение приняты на рассмотрение. Ожидайте решения. Ответ придёт Вам в виде уведомления.',
                    hover_text = 'Ожидайте ответа! ❤'
                ).receiver.add(request.user)

                JournalActions.objects.create(
                    type = ActionTypes.objects.get(id=1010200),
                    action_person = request.user,
                    action_content = 'Подана идея и/или предложение от пользователя «'+ request.user.username +'».',
                    action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')]'
                )

            if not (request.POST['type'] in ['21', '22'] and request.user.role.id == 4 and User.objects.filter(role=UserRoles.objects.get(id=4)).count() <= 1):
                contacting_support = ContactingSupport.objects.create(title=title, type=ContactingSupportTypes.objects.get(id=request.POST['type']), asked_by=request.user, ask_content=request.POST['desc'], ask_additional_info=ask_additional_info, when_asked=timezone.now())
                if request.FILES:
                    fs = FileSystemStorage()
                    photos = request.FILES.getlist('photos')
                    i_count = 0
                    for i in photos:
                        fs.save(('contacting_support_media/' + photos[i_count].name), photos[i_count])
                        ContactingSupportPhotos.objects.create(contacting_support_action=contacting_support, photo=('contacting_support_media/' + photos[i_count].name))
                        i_count +=1

            return redirect('/')

    title = 'Обращение в поддержку'
    form = SendToSupportForm()
    context = {
        'title': title,
        'form': form,
    }
    return render(request, 'authapp/send_to_support.html', context)


#   поиск среди пользователей и публикаций
def Search(request):
    if not 'search_input' in request.GET:
        return redirect('/')
    #   сделать поиск также и по услугам

    looking_for = request.GET['search_input'].lower()

    finded_accounts = User.objects.filter(id__in=[user.id for user in User.objects.all() if looking_for in str(user.username).lower() or looking_for in str(user.bio).lower()])
    finded_pubs = Publication.objects.filter(id__in=[pub.id for pub in Publication.objects.filter(type__in=[11, 21, 31]) if looking_for in str(pub.title).lower() or looking_for in str(pub.content).lower()])
    saved_pubs_urls = SavedPubs.objects.filter(saver=request.user) if request.user.is_authenticated else []
    saved_finded_pubs = [sp.pub.id for sp in saved_pubs_urls]

    finded_accounts_count = finded_accounts.count()
    finded_pubs_count = finded_pubs.count()
    finded_count = finded_accounts_count + finded_pubs_count
    title = 'Найдено ' + str(finded_count) + ' результатов по запросу «' + looking_for +'»' if finded_count else 'Ничего не найдено по запросу «' + looking_for +'»'

    if request.user.is_authenticated:
        JournalActions.objects.create(
            type = ActionTypes.objects.get(id=3090200),
            action_person = request.user,
            action_content = 'Поисковый запрос '+ request.GET['search_input'] +' пользователем «'+ request.user.username +'».',
            action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')]'
        )

    context = {
        'looking_for': looking_for,
        'finded_count': finded_count,
        'finded_accounts': finded_accounts,
        'finded_accounts_count': finded_accounts_count,
        'finded_pubs': finded_pubs,
        'saved_finded_pubs': saved_finded_pubs,
        'finded_pubs_count': finded_pubs_count,
        'title': title,
    }
    return render(request, 'authapp/search_results.html', context)
