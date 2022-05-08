from django.db.models import Q
# from django.db.models.functions import Lower

from django.shortcuts import render, redirect

from django.views.generic.list import ListView
from django.views.generic import TemplateView, UpdateView

from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView, LogoutView
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, HttpResponseNotFound, Http404
from django.urls import reverse, reverse_lazy

from authapp.forms import RegisterForm, LoginForm
from authapp.models import *
from publicationapp.models import *
from .forms import *
from django.utils import timezone

from phonenumber_field.phonenumber import PhoneNumber


#   удаление учётной записи пользователя
def DeleteAccount(request, pk):
    if request.user.is_authenticated:
        user = User.objects.get(id=pk)
        if request.user.id == user.id or request.user.role.id == 4:
            user_id = user.id
            user_name = user.username
            user_photo = user.photo.name
            user.delete()

            if request.user.id != user_id:
                noti=Publication.objects.create(title=('Успешно удалён пользователь ' + user_name), type=PubTypes.objects.get(id=51), preview=(user_photo), content="Вот и зачем Вы его так?", author=request.user)
                Notifications.objects.create(user_receiver=request.user, noti_for_user=noti)
                return redirect('admin_mine:users')
            else:
                return redirect('auth:logout')


#   включение-отключение получение уведомлений от автора
def toggle_get_noti_from_author(request, pk):
    if request.is_ajax():
        if request.user.is_authenticated:
            duplicate = UserSubscribes.objects.filter(subscriber_id=request.user, star_id=pk)

            if not duplicate:
                if request.user != User.objects.get(id=pk):
                    record = UserSubscribes.objects.create(subscriber_id=request.user, star_id=User.objects.get(id=pk))
                    record.save()
                    result = 1
                    noti=Publication.objects.create(title=('Пользователь '+ request.user.username +' подписался на уведомления о Ваших новых публикациях.'), type=PubTypes.objects.get(id=51), preview=(request.user.photo.name), content=("Теперь у Вас " + str( UserSubscribes.objects.filter(star_id=pk).count() ) + " подписчиков"), author=request.user)
                    Notifications.objects.create(user_receiver=User.objects.get(id=pk), noti_for_user=noti)
                    noti=Publication.objects.create(title=('Теперь вы будете получить уведомления о новых публикациях пользователя '+ User.objects.get(id=pk).username), type=PubTypes.objects.get(id=51), preview=(User.objects.get(id=pk).photo.name), content=("Теперь у Вас " + str( UserSubscribes.objects.filter(subscriber_id=request.user.id).count() ) + " источников уведомлений о публикациях"), author=request.user)
                    Notifications.objects.create(user_receiver=request.user, noti_for_user=noti)
                else:
                    result = 0
                    noti=Publication.objects.create(title=('Вы пытались подписаться сами на себя. Давайте так не делать :)'), type=PubTypes.objects.get(id=51), preview=(request.user.photo.name), content=("Не ну а шо вы в самый раз"), author=request.user)
                    Notifications.objects.create(user_receiver=request.user, noti_for_user=noti)
            else:
                duplicate.delete()
                result = 0

            # context = {
            #     'user': request.user,
            #     'news_item': NewsItem.objects.get(pk=pk)
            # }
            # result = render_to_string('newsapp/includes/likes_block.html', context)
            return JsonResponse({'result': result})


#   получение сигнала о том,
#   что новые уведомления открыты и прочитаны
def new_noti_were_seen(request, pk):
    if request.is_ajax():
        if Notifications.objects.filter(user_receiver=request.user, is_new=True):
            result = 1
            for nn in Notifications.objects.filter(user_receiver=request.user, is_new=True):
                nn.is_new = False
                nn.save()
        else:
            result = 0
        return JsonResponse({'result': result})


#   авторизация пользователя
class UserLoginView(LoginView):
    template_name = "authapp/login.html"
    model = User
    title ='Вход в ИС'
    success_url = reverse_lazy('main')
    form_class = LoginForm

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return redirect('main')
        else:
            return 1


#   выход из учётной записи пользователя
class UserLogoutView(LogoutView):
    next_page = reverse_lazy('main')


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
                form.save()
                return HttpResponseRedirect(reverse('auth:login'))

        content = {
            'title': 'Регистрация',
            'form': form,
        }
        return render(request, self.template_name, content)


#   просмотр одной странички пользователя
class AccountOneWatch(ListView):
    model = User
    template_name = 'authapp/user_one.html'
    context_object_name = 'opened_user'
    allow_empty = False # сделать ответ на случай, если публикации с введённым id не существует

    def get_queryset(self):
        return User.objects.get(id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(AccountOneWatch, self).get_context_data(**kwargs)

        opened_user = User.objects.get(id=self.kwargs['pk'])
        opened_user.seen_count +=1
        opened_user.save()
        user_role = opened_user.role.id

        saved_pubs = subscribing_authors  = None
        if self.request.user.is_authenticated:
            saved_urls = SavedPubs.objects.filter(saver_id=self.request.user)
            saved_pubs = [sp.pub_id.id for sp in saved_urls]
            subscribes_urls = UserSubscribes.objects.filter(subscriber_id=self.request.user)
            subscribing_authors = [sa.star_id.id for sa in subscribes_urls]

        expert_info = expert_pubs = None
        if user_role in [2, 4]:
            expert_pubs = Publication.objects.filter(author=self.kwargs['pk'], type__id__in=[11, 21, 31])
            try:
                expert_info = ExpertInfo.objects.get(expert_id=self.kwargs['pk'])

            except ObjectDoesNotExist:
                expert_info = None


        context.update({
            'expert_info': expert_info,
            'expert_pubs': expert_pubs,
            'saved_pubs': saved_pubs,
            'subscribing_authors': subscribing_authors,
        })
        return context


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
    edited_user_subs = UserSubscribes.objects.filter(subscriber_id=pk)

    if edited_user.role.id == 2:
        edited_user_expert_info = ExpertInfo.objects.get(expert_id=pk) if ExpertInfo.objects.filter(expert_id=pk) else ExpertInfo.objects.create(expert_id=edited_user).save()
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

        if User.objects.filter(phone_number=request.POST['phone_number']).exclude(id=pk):
            form_user.add_error('phone_number', 'Пользователь с таким номером телефона уже существует. Пожалуйста, введите иной.')

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

            if (edited_user.role.id == 2) or ('role' in method_POST and request.user.role.id == 4):
                if 'role' in method_POST:
                    if method_POST['role'] == "4" and User.objects.filter(role=UserRoles.objects.get(id=4)).count() > 1:
                        edited_user.role = edited_user.role
                    else:
                        edited_user.role = UserRoles.objects.get(id=method_POST['role'])

                edited_user_expert_info = ExpertInfo.objects.get(expert_id=pk) if ExpertInfo.objects.filter(expert_id=pk) else ExpertInfo.objects.create(expert_id=edited_user)
                edited_user_expert_info.__dict__.update({
                    'knowledge': method_POST['knowledge'],
                    'offer': method_POST['offer'],
                    'site': method_POST['site'],
                    'bisness_phone_number': method_POST['bisness_phone_number'],
                    'address': method_POST['address'],
                    'telegram': method_POST['telegram'],
                    'whatsapp': method_POST['whatsapp'],
                    'viber': method_POST['viber'],
                    'lol': method_POST['lol'],
                    'vk': method_POST['vk'],
                    'inst': method_POST['inst'],
                    'ok': method_POST['ok'],
                    'twitter': method_POST['twitter'],
                    'other': method_POST['other'],
                    })
                edited_user_expert_info.save()

            edited_user.save()

            if request.user.id == edited_user.id:
                noti=Publication.objects.create(title=('Аккаунт успешно отредактирован.'), type=PubTypes.objects.get(id=51), preview=(edited_user.photo.name), content=("Вы большой молодец"), author=request.user)
                Notifications.objects.create(user_receiver=request.user, noti_for_user=noti)
            else:
                noti=Publication.objects.create(title=('Успешно отредактирован аккаунт пользователя '+ edited_user.username), type=PubTypes.objects.get(id=51), preview=(edited_user.photo.name), content=("Вы большой молодец"), author=request.user)
                Notifications.objects.create(user_receiver=request.user, noti_for_user=noti)
                noti=Publication.objects.create(title=('Ваш аккаунт отредактирован суперпользователем '+ request.user.username), type=PubTypes.objects.get(id=51), preview=(edited_user.photo.name), content=("Вы большой молодец"), author=request.user)
                Notifications.objects.create(user_receiver=edited_user, noti_for_user=noti)

            return redirect('auth:account_one', pk=edited_user.id)

    title = 'Настройки пользователя' if request.user.id == int(pk) else 'Настройки пользователя ' + edited_user.username
    context = {
        'title': title,
        'form_user': form_user,
        'form_expert_user': form_expert_user,
        'edited_user': edited_user,
        'edited_user_subs': edited_user_subs,
    }
    return render(request, 'authapp/update_account.html', context)


#   создание учётной записи пользователя суперадмином
def CreateAccount(request):
    if not request.user.is_authenticated:
        return redirect('main')
    if not request.user.role.id == 4:
        return redirect('main')

    edited_user = None
    form_user = UserForm()
    form_expert_user = UserExpertForm()

    if request.method == 'POST':
        form_user = UserForm(request.POST)
        if form_user.is_valid():
            method_POST = request.POST
            edited_user = User.objects.create(
                username=method_POST['username'],
                age=method_POST['age'],
                phone_number=method_POST['phone_number'],
                role=UserRoles.objects.get(id=method_POST['role'])
                )

            if 'photo' in request.FILES:
                edited_user.__dict__.update({
                    'photo': ('users_avatars/' + str(request.FILES['photo'])),
                    })
                fs = FileSystemStorage()
                photo_file = fs.save(('users_avatars/' + request.FILES['photo'].name), request.FILES['photo'])

            edited_user.save()
            if method_POST['role'] in [2, "2"]:
                edited_user_expert_info = ExpertInfo.objects.filter(expert_id=edited_user.id)
                edited_user_expert_info = ExpertInfo.objects.get(expert_id=edited_user.id) if edited_user_expert_info else ExpertInfo.objects.create(expert_id=edited_user)
                edited_user_expert_info.__dict__.update({
                    'knowledge': method_POST['knowledge'],
                    'offer': method_POST['offer'],
                    'bisness_phone_number': method_POST['bisness_phone_number'],
                    'site': method_POST['site'],
                    'address': method_POST['address'],
                    'telegram': method_POST['telegram'],
                    'whatsapp': method_POST['whatsapp'],
                    'viber': method_POST['viber'],
                    'lol': method_POST['lol'],
                    'vk': method_POST['vk'],
                    'inst': method_POST['inst'],
                    'ok': method_POST['ok'],
                    'twitter': method_POST['twitter'],
                    'other': method_POST['other'],
                    })
                edited_user_expert_info.save()

            noti=Publication.objects.create(title=('Успешно создан аккаунт пользователя '+ edited_user.username), type=PubTypes.objects.get(id=51), preview=(edited_user.photo.name), content=("Вы большой молодец, что расширяете нам базу пользователей"), author=request.user)
            Notifications.objects.create(user_receiver=request.user, noti_for_user=noti)

            return redirect('auth:account_one', pk=edited_user.id)

    title = 'Создать нового пользователя'
    context = {
        'title': title,
        'form_user': form_user,
        'form_expert_user': form_expert_user,
        'edited_user': edited_user,
    }
    return render(request, 'authapp/create_new_account.html', context)


#   подать заявку на аминистратора
def BecomeATeammember(request):
    if not request.user.is_authenticated:
        return HttpResponse("Вы ещё не авторизированы, Вам стоит сначала <a href='/account/login/'>авторизоваться</a>. <a href='/'>На главную</a>")
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

            noti=Publication.objects.create(title=('Ваша заявка стать участником команды принята на рассмотрение. О нашем решении Вы узнаете через уведомление. Скоро Вы увидите здесь ответ.'), type=PubTypes.objects.get(id=51), preview=(request.user.photo.name), content="Ожидайте ответа!", author=request.user)
            Notifications.objects.create(user_receiver=request.user, noti_for_user=noti)
            return redirect('/')

    title = 'Стать частью команды «Ремонт и дизайн»'
    form = BecomeATeammemberForm()
    context = {
        'title': title,
        'form': form,
    }
    return render(request, 'authapp/become_a_teammemder.html', context)


#   подать заявку на автора
def BecomeAnAuthor(request):
    if not request.user.is_authenticated:
        return HttpResponse("Вы ещё не авторизированы, Вам стоит сначала <a href='/account/login/'>авторизоваться</a>. <a href='/'>На главную</a>")
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

            if request.POST['knowledge'] or request.POST['offer'] or request.POST['site'] or request.POST['address'] or request.POST['telegram'] or request.POST['whatsapp'] or request.POST['viber'] or request.POST['vk'] or request.POST['inst'] or request.POST['ok'] or request.POST['twitter'] or request.POST['other']:
                becomer_expert_info = ExpertInfo.objects.filter(expert_id=request.user.id)
                if becomer_expert_info:
                    becomer_expert_info = ExpertInfo.objects.get(expert_id=request.user.id)
                else:
                    becomer_expert_info = ExpertInfo.objects.create(expert_id=request.user)
                becomer_expert_info.__dict__.update({
                    'knowledge': request.POST['knowledge'],
                    'offer': request.POST['offer'],
                    'site': request.POST['site'],
                    'address': request.POST['address'],
                    'telegram': request.POST['telegram'],
                    'whatsapp': request.POST['whatsapp'],
                    'viber': request.POST['viber'],
                    'vk': request.POST['vk'],
                    'inst': request.POST['inst'],
                    'ok': request.POST['ok'],
                    'twitter': request.POST['twitter'],
                    'other': request.POST['other'],
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

            noti=Publication.objects.create(title=('Ваша заявка стать автором публикаций принята на рассмотрение. О нашем решении Вы узнаете через уведомление. Скоро Вы увидите здесь ответ.'), type=PubTypes.objects.get(id=51), preview=(request.user.photo.name), content="Ожидайте ответа!", author=request.user)
            Notifications.objects.create(user_receiver=request.user, noti_for_user=noti)
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
        return HttpResponse("Вы ещё не авторизированы, Вам стоит сначала <a href='/account/login/'>авторизоваться</a>. <a href='/'>На главную</a>")

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
                # return render(request, 'authapp/send_to_support.html', context)
                return render(request, 'authapp/send_to_support.html', context)

            ask_additional_info = 0

            if request.POST['type'] == '11':
                pub = Publication.objects.get(id=request.POST['complaint_pub_id'])
                title = 'Жалоба на публикацию «'+ pub.title + '»'
                ask_additional_info = int(request.POST['complaint_pub_id'])
                noti=Publication.objects.create(title=title+ ' принята на рассмотрение. Ожидайте решения. Ответ придёт Вам в виде уведомления.', type=PubTypes.objects.get(id=51), preview=pub.preview.name, content="Ожидайте ответа! ❤", author=request.user)
                Notifications.objects.create(user_receiver=request.user, noti_for_user=noti)
                noti=Publication.objects.create(title='Принята на рассмотрение жалоба на Вашу публикацию «'+ pub.title +'». Ожидайте решения.', type=PubTypes.objects.get(id=51), preview=pub.preview.name, content="Ожидайте ответа! ❤", author=request.user)
                Notifications.objects.create(user_receiver=pub.author, noti_for_user=noti)

            if request.POST['type'] == '12':
                account = User.objects.get(id=request.POST['complaint_account_id'])
                title = 'Жалоба на пользователя «'+ account.username + '»'
                ask_additional_info = int(request.POST['complaint_account_id'])
                noti=Publication.objects.create(title=title+ ' принята на рассмотрение. Ожидайте решения. Ответ придёт Вам в виде уведомления.', type=PubTypes.objects.get(id=51), preview=account.photo.name, content="Ожидайте ответа! ❤", author=request.user)
                Notifications.objects.create(user_receiver=request.user, noti_for_user=noti)
                noti=Publication.objects.create(title='Принята на рассмотрение жалоба на Ваш аккаунт. Ожидайте решения.', type=PubTypes.objects.get(id=51), preview=account.photo.name, content="Ожидайте ответа! ❤", author=request.user)
                Notifications.objects.create(user_receiver=account, noti_for_user=noti)

            if request.POST['type'] in ['21', '22'] and request.user.role.id == 4 and User.objects.filter(role=UserRoles.objects.get(id=4)).count() <= 1:
                noti=Publication.objects.create(title='Ваша заявка на смену роли не может быть принята на рассмотрение. На данный момент в системе всего 1 суперпользователь, поэтому нам опасно менять Вам роль. Найдите наследника и обращайтесь ещё! С заботой, Ваша поддержка «Ремонта и дизайна»', type=PubTypes.objects.get(id=51), preview=request.user.photo.name, content="По-другому пока не можем. Просим простить нас ❤", author=request.user)
                Notifications.objects.create(user_receiver=request.user, noti_for_user=noti)
                return redirect('/')

            if request.POST['type'] == '21':
                title = 'Заявка на роль автора от пользователя «'+ request.user.username + '»'
                noti=Publication.objects.create(title='Ваша заявка на роль автора принята на рассмотрение. Ожидайте решения. Ответ придёт Вам в виде уведомления.', type=PubTypes.objects.get(id=51), preview=request.user.photo.name, content="Ожидайте ответа! ❤", author=request.user)
                Notifications.objects.create(user_receiver=request.user, noti_for_user=noti)

            if request.POST['type'] == '22':
                title = 'Заявка на роль модератора от пользователя «'+ request.user.username + '»'
                noti=Publication.objects.create(title='Ваша заявка на участника команды (модератора) принята на рассмотрение. Ожидайте решения. Ответ придёт Вам в виде уведомления.', type=PubTypes.objects.get(id=51), preview=request.user.photo.name, content="Ожидайте ответа!", author=request.user)
                Notifications.objects.create(user_receiver=request.user, noti_for_user=noti)

            if request.POST['type'] == '31':
                title = 'Вопрос от пользователя «'+ request.user.username + '»'
                noti=Publication.objects.create(title='Ваш вопрос принят. Ожидайте решения. Ответ придёт Вам в виде уведомления.', type=PubTypes.objects.get(id=51), preview=request.user.photo.name, content="Ожидайте ответа! ❤", author=request.user)
                Notifications.objects.create(user_receiver=request.user, noti_for_user=noti)

            if request.POST['type'] == '32':
                title = 'Идея и/или предложение от пользователя «'+ request.user.username + '»'
                noti=Publication.objects.create(title='Ваша Идея и/или предложение приняты на рассмотрение. Ожидайте решения. Ответ придёт Вам в виде уведомления.', type=PubTypes.objects.get(id=51), preview=request.user.photo.name, content="Ожидайте ответа! ❤", author=request.user)
                Notifications.objects.create(user_receiver=request.user, noti_for_user=noti)

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

    # looking_for = Lower(request.GET['search_input'])
    looking_for = request.GET['search_input'].lower()

    # finded_experts = ExpertInfo.objects.filter(Q(knowledge__icontains=looking_for) | Q(offer__icontains=looking_for))
    # finded_experts_list_id = []
    # for expert in finded_experts:
    #     finded_experts_list_id.append(expert.expert_id.id)
    # finded_accounts = User.objects.filter(Q(username__icontains=looking_for) | Q(bio__icontains=looking_for) | Q(id__in=finded_experts_list_id))
    finded_accounts = User.objects.filter(id__in=[user.id for user in User.objects.all() if looking_for in str(user.username).lower() or looking_for in str(user.bio).lower()])
    finded_pubs = Publication.objects.filter(id__in=[pub.id for pub in Publication.objects.filter(type__in=[11, 21, 31]) if looking_for in str(pub.title).lower() or looking_for in str(pub.content).lower()])
    saved_pubs_urls = SavedPubs.objects.filter(saver_id=request.user) if request.user.is_authenticated else []
    saved_finded_pubs = [sp.pub_id.id for sp in saved_pubs_urls]
    subscribing_authors = [sa.star_id.id for sa in (UserSubscribes.objects.filter(subscriber_id=request.user))] if request.user.is_authenticated else None

    finded_accounts_count = finded_accounts.count()
    finded_pubs_count = finded_pubs.count()
    finded_count = finded_accounts_count + finded_pubs_count
    title = 'Найдено ' + str(finded_count) + ' результатов по запросу «' + looking_for +'»' if finded_count else 'Ничего не найдено по запросу «' + looking_for +'»'

    context = {
        'looking_for': looking_for,
        'finded_count': finded_count,
        'finded_accounts': finded_accounts,
        'finded_accounts_count': finded_accounts_count,
        'finded_pubs': finded_pubs,
        'saved_finded_pubs': saved_finded_pubs,
        'subscribing_authors': subscribing_authors,
        'finded_pubs_count': finded_pubs_count,
        'title': title,
    }
    return render(request, 'authapp/search_results.html', context)
