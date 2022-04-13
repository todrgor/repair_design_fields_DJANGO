from django.db.models import Q

from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from django.views.generic.list import ListView

from django.contrib.auth import logout, login
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, UpdateView
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, HttpResponseNotFound, Http404

from authapp.forms import RegisterForm, LoginForm
from authapp.models import *
from publicationapp.models import *
from .forms import *
from django.utils import timezone

# удаление учётной записи пользователя
def DeleteAccount(request, pk):
    if request.user.is_authenticated:
        user = User.objects.get(id=pk)
        if request.user.id == user.id or request.user.role.id == 4:
            user_id = user.id
            user_name = user.username
            user_photo = user.photo.name
            user.delete()

            if request.user.role.id != user_id:
                noti=Publication.objects.create(title=('Успешно удалён пользователь ' + user_name), role=PubRoles.objects.get(id=51), preview=(user_photo), content_first_desc="Вот и зачем Вы его так?", content_last_desc='', author=request.user)
                Notifications.objects.create(user_receiver=request.user, noti_for_user=noti)
                return redirect('admin_mine:users')
            else:
                return redirect('auth:logout')

# включение-отключение получение уведомлений от автора
def toggle_get_noti_from_author(request, pk):
    if request.is_ajax():
        if request.user.is_authenticated:
            duplicate = UserSubscribes.objects.filter(subscriber_id=request.user, star_id=pk)

            if not duplicate:
                record = UserSubscribes.objects.create(subscriber_id=request.user, star_id=User.objects.get(id=pk))
                record.save()
                result = 1

                noti=Publication.objects.create(title=('Пользователь '+ request.user.username +' подписался на уведомления о Ваших новых публикациях.'), role=PubRoles.objects.get(id=51), preview=(request.user.photo.name), content_first_desc=("Теперь у Вас " + str( UserSubscribes.objects.filter(star_id=pk).count() ) + " подписчиков"), content_last_desc='', author=request.user)
                Notifications.objects.create(user_receiver=User.objects.get(id=pk), noti_for_user=noti)
                noti=Publication.objects.create(title=('Теперь вы будете получить уведомления о новых публикациях пользователя '+ User.objects.get(id=pk).username), role=PubRoles.objects.get(id=51), preview=(User.objects.get(id=pk).photo.name), content_first_desc=("Теперь у Вас " + str( UserSubscribes.objects.filter(subscriber_id=request.user.id).count() ) + " источников уведомлений о публикациях"), content_last_desc='', author=request.user)
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


# получение сигнала о том,
# что новые уведомления открыты и прочитаны
def new_noti_were_seen(request, pk):
    if request.is_ajax():
        if Notifications.objects.filter(user_receiver=request.user, is_new=True):
            for nn in Notifications.objects.filter(user_receiver=request.user, is_new=True):
                nn.is_new = False
                nn.save()
            result = 1
        else:
            result = 0
        return JsonResponse({'result': result})


# авторизация пользователя
class UserLoginView(LoginView):
    template_name = "authapp/login.html"
    model = User
    title ='Вход в ИС'
    success_url = reverse_lazy('main')
    form_class = LoginForm


# выход из учётной записи пользователя
class UserLogoutView(LogoutView):
    next_page = reverse_lazy('main')


# регистрация пользователя
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
            'form': form,
        }
        return render(request, self.template_name, content)


# просмотр одной странички пользователя
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

        user_role = User.objects.get(id=self.kwargs['pk']).role.id
        if self.request.user.is_authenticated:
            saved_urls = SavedPubs.objects.filter(saver_id=self.request.user)
            saved_pubs = [sp.pub_id.id for sp in saved_urls]
            subscribes_urls = UserSubscribes.objects.filter(subscriber_id=self.request.user)
            subscribing_authors = [sa.star_id.id for sa in subscribes_urls]

        else:
            saved_pubs = subscribing_authors  = None

        if user_role == 2 or user_role == 4:
            try:
                expert_info = ExpertInfo.objects.get(expert_id=self.kwargs['pk'])
                if expert_info.knowledge or expert_info.site or expert_info.site or expert_info.address or expert_info.whatsapp or expert_info.viber or expert_info.vk or expert_info.inst or expert_info.ok or expert_info.fb or expert_info.other:
                    expert_info = expert_info
                else:
                    expert_info = None

            except ObjectDoesNotExist:
                expert_info = None

            expert_pubs = Publication.objects.filter(author=self.kwargs['pk'], role__id__in=[11, 21, 31])
            pub_has_tags = PubHasTags.objects.filter(pub_id__in=expert_pubs)
        else:
            expert_info = None
            expert_pubs = None
            pub_has_tags = None

        context.update({
            'expert_info': expert_info,
            'expert_pubs': expert_pubs,
            'pub_has_tags': pub_has_tags,
            'saved_pubs': saved_pubs,
            'subscribing_authors': subscribing_authors,
        })
        return context


# изменение учётной записи пользователя
def UpdateAccount(request, pk):
    if request.user.is_authenticated:
        if request.user.role.id == 4 or request.user.id == int(pk):
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
            if request.method == 'POST':
                form_user = UserForm(request.POST)
                edited_user_post = request.POST
                if 'photo' in request.FILES:
                    edited_user.__dict__.update({'username': edited_user_post['username'], 'photo': ('users_avatars/' + str(request.FILES['photo'])), 'bio': edited_user_post['bio'], 'age': edited_user_post['age'], 'phone_number': edited_user_post['phone_number'], })
                    fs = FileSystemStorage()
                    photo_file = fs.save(('users_avatars/' + request.FILES['photo'].name), request.FILES['photo'])
                else:
                    edited_user.__dict__.update({'username': edited_user_post['username'], 'bio': edited_user_post['bio'], 'age': edited_user_post['age'], 'phone_number': edited_user_post['phone_number'], })
                edited_user.save()
                if 'role' in edited_user_post:
                    if edited_user_post['role'] == 2 or edited_user_post['role'] == "2":
                        edited_user.role = UserRoles.objects.get(id=2)
                        edited_user.save()
                        edited_user_expert_info = ExpertInfo.objects.filter(expert_id=pk)
                        if edited_user_expert_info:
                            edited_user_expert_info = ExpertInfo.objects.get(expert_id=pk)
                        else:
                            edited_user_expert_info = ExpertInfo.objects.create(expert_id=edited_user)
                        edited_user_expert_info.__dict__.update({'knowledge': edited_user_post['knowledge'], 'offer': edited_user_post['offer'], 'site': edited_user_post['site'], 'address': edited_user_post['address'], 'telegram': edited_user_post['telegram'], 'whatsapp': edited_user_post['whatsapp'], 'viber': edited_user_post['viber'], 'vk': edited_user_post['vk'], 'inst': edited_user_post['inst'], 'ok': edited_user_post['ok'], 'fb': edited_user_post['fb'], 'other': edited_user_post['other'], })
                        edited_user_expert_info.save()

                if request.user.id == edited_user.id:
                    noti=Publication.objects.create(title=('Аккаунт успешно отредактирован.'), role=PubRoles.objects.get(id=51), preview=(edited_user.photo.name), content_first_desc=("Вы большой молодец"), content_last_desc='', author=request.user)
                    Notifications.objects.create(user_receiver=request.user, noti_for_user=noti)
                else:
                    noti=Publication.objects.create(title=('Успешно отредактирован аккаунт пользователя '+ edited_user.username), role=PubRoles.objects.get(id=51), preview=(edited_user.photo.name), content_first_desc=("Вы большой молодец"), content_last_desc='', author=request.user)
                    Notifications.objects.create(user_receiver=request.user, noti_for_user=noti)
                    noti=Publication.objects.create(title=('Ваш аккаунт отредактирован суперпользователем '+ request.user.username), role=PubRoles.objects.get(id=51), preview=(edited_user.photo.name), content_first_desc=("Вы большой молодец"), content_last_desc='', author=request.user)
                    Notifications.objects.create(user_receiver=edited_user, noti_for_user=noti)

                return redirect('auth:account_one', pk=edited_user.id)

            if request.user.id == int(pk):
                title = 'Настройки пользователя'
            else:
                title = 'Настройки пользователя ' + edited_user.username
            context = {
                'title': title, 'form_user': form_user,
                'form_user_expert': form_user_expert,
                'edited_user': edited_user,
                'edited_user_subs': edited_user_subs,
            }
            return render(request, 'authapp/update_account.html', context)
        else:
            return redirect('main')
    else:
        return redirect('main')


# создание учётной записи пользователя суперадмином
def CreateAccount(request):
    if request.user.is_authenticated:
        edited_user = None
        if request.user.role.id == 4:
            form_user = UserForm()
            form_user_expert = UserExpertForm()
            if request.method == 'POST':
                print(request.POST['role'])
                form_user = UserForm(request.POST)
                edited_user_post = request.POST
                edited_user = User.objects.create(username=edited_user_post['username'], age=edited_user_post['age'], phone_number=edited_user_post['phone_number'], role=UserRoles.objects.get(id=edited_user_post['role']) )
                if 'photo' in request.FILES:
                    edited_user.__dict__.update({'username': edited_user_post['username'], 'photo': ('users_avatars/' + str(request.FILES['photo'])), 'bio': edited_user_post['bio'], 'age': edited_user_post['age'], 'phone_number': edited_user_post['phone_number'], })
                    fs = FileSystemStorage()
                    photo_file = fs.save(('users_avatars/' + request.FILES['photo'].name), request.FILES['photo'])
                else:
                    edited_user.__dict__.update({'username': edited_user_post['username'], 'bio': edited_user_post['bio'], 'age': edited_user_post['age'], 'phone_number': edited_user_post['phone_number'], })
                edited_user.save()
                if edited_user_post['role'] == 2 or edited_user_post['role'] == "2":
                    edited_user_expert_info = ExpertInfo.objects.filter(expert_id=edited_user.id)
                    if edited_user_expert_info:
                        edited_user_expert_info = ExpertInfo.objects.get(expert_id=edited_user.id)
                    else:
                        edited_user_expert_info = ExpertInfo.objects.create(expert_id=edited_user)
                        edited_user_expert_info.save()
                    edited_user_expert_info.__dict__.update({'knowledge': edited_user_post['knowledge'], 'offer': edited_user_post['offer'], 'site': edited_user_post['site'], 'address': edited_user_post['address'], 'telegram': edited_user_post['telegram'], 'whatsapp': edited_user_post['whatsapp'], 'viber': edited_user_post['viber'], 'vk': edited_user_post['vk'], 'inst': edited_user_post['inst'], 'ok': edited_user_post['ok'], 'fb': edited_user_post['fb'], 'other': edited_user_post['other'], })
                    edited_user_expert_info.save()

                noti=Publication.objects.create(title=('Успешно создан аккаунт пользователя '+ edited_user.username), role=PubRoles.objects.get(id=51), preview=(edited_user.photo.name), content_first_desc=("Вы большой молодец, что расширяете нам базу пользователей"), content_last_desc='', author=request.user)
                Notifications.objects.create(user_receiver=request.user, noti_for_user=noti)

                return redirect('auth:account_one', pk=edited_user.id)

            title = 'Создать нового пользователя'

            context = {
                'title': title,
                'form_user': form_user,
                'form_user_expert': form_user_expert,
                'edited_user': edited_user,
            }
            return render(request, 'authapp/create_new_account.html', context)
        else:
            return redirect('main')
    else:
        return redirect('main')


# подать заявку на аминистратора
def BecomeATeammember(request):
    if request.user.role.id == 3:
        return HttpResponse("Вы уже участник нашей команды, Вам не нужно подаввать заявку на свою же роль. Ну вот зачем?")

    if request.method == 'POST':
        if request.POST['desc']:
            contacting_support = ContactingSupport.objects.create(title=('Заявка на роль модератора от пользвователя «' + request.user.username +'»'), role=ContactingSupportTypes.objects.get(id=22), asked_by=request.user, ask_content=request.POST['desc'], ask_additional_info='', when_asked=timezone.now())
            if request.FILES:
                fs = FileSystemStorage()
                photos = request.FILES.getlist('photos')
                i_count = 0
                for i in photos:
                    fs.save(('contacting_support_media/' + photos[i_count].name), photos[i_count])
                    ContactingSupportPhotos.objects.create(contacting_support_action=contacting_support, photo=('contacting_support_media/' + photos[i_count].name))
                    i_count +=1

            noti=Publication.objects.create(title=('Ваша заявка стать участником команды принята на рассмотрение. О нашем решении Вы узнаете через уведомление. Скоро Вы увидите здесь ответ.'), role=PubRoles.objects.get(id=51), preview=(request.user.photo.name), content_first_desc="Ожидайте ответа!", content_last_desc='', author=request.user)
            Notifications.objects.create(user_receiver=request.user, noti_for_user=noti)
            return redirect('/')

    title = 'Стать частью команды «Ремонт и дизайн»'
    form = BecomeATeammemberForm()
    context = {
        'title': title,
        'form': form,
    }
    return render(request, 'authapp/become_a_teammemder.html', context)


# подать заявку на автора
def BecomeAnAuthor(request):
    if request.user.role.id == 2:
        return HttpResponse("Вы уже автор публикаций, Вам не нужно подаввать заявку на свою же роль. Ну вот зачем?")

    if request.method == 'POST':
        if request.POST['desc']:
            contacting_support = ContactingSupport.objects.create(title=('Заявка на роль автора от пользвователя «' + request.user.username +'»'), role=ContactingSupportTypes.objects.get(id=21), asked_by=request.user, ask_content=request.POST['desc'], ask_additional_info='', when_asked=timezone.now())

            if request.POST['knowledge'] or request.POST['offer'] or request.POST['site'] or request.POST['address'] or request.POST['telegram'] or request.POST['whatsapp'] or request.POST['viber'] or request.POST['vk'] or request.POST['inst'] or request.POST['ok'] or request.POST['fb'] or request.POST['other']:
                becomer_expert_info = ExpertInfo.objects.filter(expert_id=request.user.id)
                if becomer_expert_info:
                    becomer_expert_info = ExpertInfo.objects.get(expert_id=request.user.id)
                else:
                    becomer_expert_info = ExpertInfo.objects.create(expert_id=request.user)
                becomer_expert_info.__dict__.update({'knowledge': request.POST['knowledge'], 'offer': request.POST['offer'], 'site': request.POST['site'], 'address': request.POST['address'], 'telegram': request.POST['telegram'], 'whatsapp': request.POST['whatsapp'], 'viber': request.POST['viber'], 'vk': request.POST['vk'], 'inst': request.POST['inst'], 'ok': request.POST['ok'], 'fb': request.POST['fb'], 'other': request.POST['other'], })
                becomer_expert_info.save()

            if request.FILES:
                fs = FileSystemStorage()
                photos = request.FILES.getlist('photos')
                i_count = 0
                for i in photos:
                    fs.save(('contacting_support_media/' + photos[i_count].name), photos[i_count])
                    ContactingSupportPhotos.objects.create(contacting_support_action=contacting_support, photo=('contacting_support_media/' + photos[i_count].name))
                    i_count +=1

            noti=Publication.objects.create(title=('Ваша заявка стать автором публикаций принята на рассмотрение. О нашем решении Вы узнаете через уведомление. Скоро Вы увидите здесь ответ.'), role=PubRoles.objects.get(id=51), preview=(request.user.photo.name), content_first_desc="Ожидайте ответа!", content_last_desc='', author=request.user)
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


# подать обращение в поддержку: жалоба на пабликацию
# или пользователя, заявка на автора публикаций
# или администратора, а также вопрос или идея/предложение
def SendToSupport(request):
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
                noti=Publication.objects.create(title=title+ ' принята на рассмотрение. Ожидайте решения. Ответ придёт Вам в виде уведомления.', role=PubRoles.objects.get(id=51), preview=pub.preview.name, content_first_desc="Ожидайте ответа!", content_last_desc='', author=request.user)
                Notifications.objects.create(user_receiver=request.user, noti_for_user=noti)
                noti=Publication.objects.create(title='Принята на рассмотрение жалоба на Вашу публикацию «'+ pub.title +'». Ожидайте решения.', role=PubRoles.objects.get(id=51), preview=pub.preview.name, content_first_desc="Ожидайте ответа!", content_last_desc='', author=request.user)
                Notifications.objects.create(user_receiver=pub.author, noti_for_user=noti)

            if request.POST['type'] == '12':
                account = User.objects.get(id=request.POST['complaint_account_id'])
                title = 'Жалоба на пользователя «'+ account.username + '»'
                ask_additional_info = int(request.POST['complaint_account_id'])
                noti=Publication.objects.create(title=title+ ' принята на рассмотрение. Ожидайте решения. Ответ придёт Вам в виде уведомления.', role=PubRoles.objects.get(id=51), preview=account.photo.name, content_first_desc="Ожидайте ответа!", content_last_desc='', author=request.user)
                Notifications.objects.create(user_receiver=request.user, noti_for_user=noti)
                noti=Publication.objects.create(title='Принята на рассмотрение жалоба на Ваш аккаунт. Ожидайте решения.', role=PubRoles.objects.get(id=51), preview=account.photo.name, content_first_desc="Ожидайте ответа!", content_last_desc='', author=request.user)
                Notifications.objects.create(user_receiver=account, noti_for_user=noti)

            if request.POST['type'] == '21':
                title = 'Заявка на роль автора от пользователя «'+ request.user.username + '»'
                noti=Publication.objects.create(title='Ваша заявка на роль автора принята на рассмотрение. Ожидайте решения. Ответ придёт Вам в виде уведомления.', role=PubRoles.objects.get(id=51), preview=request.user.photo.name, content_first_desc="Ожидайте ответа!", content_last_desc='', author=request.user)
                Notifications.objects.create(user_receiver=request.user, noti_for_user=noti)

            if request.POST['type'] == '22':
                title = 'Заявка на роль модератора от пользователя «'+ request.user.username + '»'
                noti=Publication.objects.create(title='Ваша заявка на участника команды (модератора) принята на рассмотрение. Ожидайте решения. Ответ придёт Вам в виде уведомления.', role=PubRoles.objects.get(id=51), preview=request.user.photo.name, content_first_desc="Ожидайте ответа!", content_last_desc='', author=request.user)
                Notifications.objects.create(user_receiver=request.user, noti_for_user=noti)

            if request.POST['type'] == '31':
                title = 'Вопрос от пользователя «'+ request.user.username + '»'
                noti=Publication.objects.create(title='Ваш вопрос принят. Ожидайте решения. Ответ придёт Вам в виде уведомления.', role=PubRoles.objects.get(id=51), preview=request.user.photo.name, content_first_desc="Ожидайте ответа!", content_last_desc='', author=request.user)
                Notifications.objects.create(user_receiver=request.user, noti_for_user=noti)

            if request.POST['type'] == '32':
                title = 'Идея и/или предложение от пользователя «'+ request.user.username + '»'
                noti=Publication.objects.create(title='Ваша Идея и/или предложение приняты на рассмотрение. Ожидайте решения. Ответ придёт Вам в виде уведомления.', role=PubRoles.objects.get(id=51), preview=request.user.photo.name, content_first_desc="Ожидайте ответа!", content_last_desc='', author=request.user)
                Notifications.objects.create(user_receiver=request.user, noti_for_user=noti)

            contacting_support = ContactingSupport.objects.create(title=title, role=ContactingSupportTypes.objects.get(id=request.POST['type']), asked_by=request.user, ask_content=request.POST['desc'], ask_additional_info=ask_additional_info, when_asked=timezone.now())
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


# поиск чего-либо
def Search(request):
    if 'search_input' in request.GET:
        looking_for = request.GET['search_input']

        # finded_experts = ExpertInfo.objects.filter(Q(knowledge__icontains=looking_for) | Q(offer__icontains=looking_for))
        # finded_experts_list_id = []
        # for expert in finded_experts:
        #     finded_experts_list_id.append(expert.expert_id.id)
        # finded_accounts = User.objects.filter(Q(username__icontains=looking_for) | Q(bio__icontains=looking_for) | Q(id__in=finded_experts_list_id))
        finded_accounts = User.objects.filter(Q(username__icontains=looking_for) | Q(bio__icontains=looking_for))
        finded_pubs = Publication.objects.filter(Q(title__icontains=looking_for) | Q(content_first_desc__icontains=looking_for) | Q(content_last_desc__icontains=looking_for), role__in=[11, 21, 31])
        saved_pubs_urls = SavedPubs.objects.filter(saver_id=request.user)
        saved_finded_pubs = [sp.pub_id.id for sp in saved_pubs_urls]
        pub_has_tags = PubHasTags.objects.filter(pub_id__role__id=31, pub_id__id__in=finded_pubs)
        subscribing_authors = [sa.star_id.id for sa in (UserSubscribes.objects.filter(subscriber_id=request.user))]

        finded_accounts_count = finded_accounts.count()
        finded_pubs_count = finded_pubs.count()
        finded_count = finded_accounts_count + finded_pubs_count

        title = 'Ничего не найдено по запросу' + looking_for
        if finded_count:
            title = 'Найдено ' + str(finded_count) + ' результатов по запросу ' + looking_for

        context = {
            'looking_for': looking_for,
            'finded_count': finded_count,
            'finded_accounts': finded_accounts,
            'finded_accounts_count': finded_accounts_count,
            'finded_pubs': finded_pubs,
            'pub_has_tags': pub_has_tags,
            'saved_finded_pubs': saved_finded_pubs,
            'subscribing_authors': subscribing_authors,
            'finded_pubs_count': finded_pubs_count,
            'title': title,
        }
        return render(request, 'authapp/search_results.html', context)
    else:
        return redirect('/')
