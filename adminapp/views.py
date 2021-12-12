from django.shortcuts import render
from authapp.models import *
from publicationapp.models import *
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse



@csrf_exempt
def NewComplaint(request):
    if request.user.is_authenticated:
        if request.is_ajax():
            complaint = request.POST
            pub_complaint = Publication.objects.get(id=complaint['complaint_id'])
            Publication.objects.create(title=('Жалоба на публикацию «' + pub_complaint.title +'»'), role=PubRoles.objects.get(id=41), preview=(pub_complaint.preview.name), content_first_desc=complaint['complaint_text'], content_last_desc=complaint['complaint_type'], author=request.user)

            noti=Publication.objects.create(title=('Ваша жалоба на публикацию '+ pub_complaint.title +' принята!'), role=PubRoles.objects.get(id=51), preview=(pub_complaint.preview.name), content_first_desc="Ждите результата здесь, в уведомлениях", content_last_desc='', author=request.user)
            Notifications.objects.create(user_receiver=request.user, noti_for_user=noti)
            return JsonResponse({'result': True})


class StartPanel(ListView):
    model =  Publication
    template_name = 'adminapp/main.html'

    def get_context_data(self, **kwargs):
        title ='Главная | Панель администратора'
        pubs = Publication.objects.filter(role__id__in=[11, 21, 31]).order_by('-pushed')[:3]
        noties = Notifications.objects.filter().order_by('-when')[:4]
        users = User.objects.filter().order_by('-last_entry')[:4]
        # applications =
        # complaints =

        old_noties = Notifications.objects.filter(user_receiver=self.request.user, is_new=False).order_by('-when')[:20]
        new_noties = Notifications.objects.filter(user_receiver=self.request.user, is_new=True).order_by('-when')
        notes_count = old_noties.count() + new_noties.count()
        new_notes_count = new_noties.count()

        data = {
            'title': title,
            'pubs': pubs,
            'noties': noties,
            'users': users,
    		# 'applications': applications,
    		# 'complaints': complaints,

            'old_noties': old_noties,
            'new_noties': new_noties,
            'notes_count': notes_count,
    		'new_notes_count': new_notes_count,
        }
        return data



class PubList(ListView):
    model =  Publication
    template_name = 'adminapp/publications.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        title ='Публикации | Панель администратора'
        pubs = Publication.objects.filter(role__id__in=[11, 21, 31])
        saved_urls = SavedPubs.objects.filter(pub_id__in = pubs)
        pub_has_tags = PubHasTags.objects.filter(pub_id__in = pubs)
        photos_urls = PubPhotos.objects.filter(id_pub__in = pubs)

        old_noties = Notifications.objects.filter(user_receiver=self.request.user, is_new=False).order_by('-when')[:20]
        new_noties = Notifications.objects.filter(user_receiver=self.request.user, is_new=True).order_by('-when')
        notes_count = old_noties.count() + new_noties.count()
        new_notes_count = new_noties.count()

        data = {
            'title': title,
            'pubs': pubs,
            'saved_urls': saved_urls,
            'pub_has_tags': pub_has_tags,
            'photos_urls': photos_urls,

            'old_noties': old_noties,
            'new_noties': new_noties,
            'notes_count': notes_count,
    		'new_notes_count': new_notes_count,
        }
        return data


class UserList(ListView):
    model =  User
    template_name = 'adminapp/users.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        title ='Пользователи | Панель администратора'
        users = User.objects.filter().order_by('-last_entry')
        saved_urls = SavedPubs.objects.filter()
        seen_urls = SeenPubs.objects.filter()
        subscribed_urls = UserSubscribes.objects.filter()
        noties = Notifications.objects.filter()

        old_noties = Notifications.objects.filter(user_receiver=self.request.user, is_new=False).order_by('-when')[:20]
        new_noties = Notifications.objects.filter(user_receiver=self.request.user, is_new=True).order_by('-when')
        notes_count = old_noties.count() + new_noties.count()
        new_notes_count = new_noties.count()

        data = {
            'title': title,
            'users': users,
            'saved_urls': saved_urls,
            'seen_urls': seen_urls,
            'subscribed_urls': subscribed_urls,
            'noties': noties,

            'old_noties': old_noties,
            'new_noties': new_noties,
            'notes_count': notes_count,
    		'new_notes_count': new_notes_count,
        }
        return data
