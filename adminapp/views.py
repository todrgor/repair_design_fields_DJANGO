from django.shortcuts import render
from authapp.models import *
from publicationapp.models import *
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse



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

    def get(self, *args, **kwargs):
        if not self.request.user.role.id in [3, 4]:
            print('проникновение туда, куда нельзя')
            return HttpResponse("Простите, но у Вас недостаточно прав для этой страницы. ")
            # return HttpResponseRedirect('/')

    def get_context_data(self, **kwargs):
        title ='Главная | Панель администратора'
        pubs = Publication.objects.filter(role__id__in=[11, 21, 31]).order_by('-pushed')[:3]
        noties = Notifications.objects.filter().order_by('-when')[:4]
        users = User.objects.filter().order_by('-last_entry')[:4]
        # applications =
        # complaints =

        data = {
            'title': title,
            'pubs': pubs,
            'noties': noties,
            'users': users,
    		# 'applications': applications,
    		# 'complaints': complaints,
        }
        return data



class PubList(ListView):
    model =  Publication
    template_name = 'adminapp/publications.html'

    def get(self, *args, **kwargs):
        if not self.request.user.role.id in [3, 4]:
            print('проникновение туда, куда нельзя')
            return HttpResponse("Простите, но у Вас недостаточно прав для этой страницы. ")
            # return HttpResponseRedirect('/')

    def get_context_data(self, *, object_list=None, **kwargs):
        title ='Публикации | Панель администратора'
        pubs = Publication.objects.filter(role__id__in=[11, 21, 31])
        saved_urls = SavedPubs.objects.filter(pub_id__in = pubs)
        pub_has_tags = PubHasTags.objects.filter(pub_id__in = pubs)
        photos_urls = PubPhotos.objects.filter(id_pub__in = pubs)

        data = {
            'title': title,
            'pubs': pubs,
            'saved_urls': saved_urls,
            'pub_has_tags': pub_has_tags,
            'photos_urls': photos_urls,
        }
        return data


class UserList(ListView):
    model =  User
    template_name = 'adminapp/users.html'

    def get(self, *args, **kwargs):
        if not self.request.user.role.id in [3, 4]:
            print('проникновение туда, куда нельзя')
            return HttpResponse("Простите, но у Вас недостаточно прав для этой страницы. ")
            # return HttpResponseRedirect('/')

    def get_context_data(self, *, object_list=None, **kwargs):
        title ='Пользователи | Панель администратора'
        users = User.objects.filter().order_by('-last_entry')
        saved_urls = SavedPubs.objects.filter()
        seen_urls = SeenPubs.objects.filter()
        subscribed_urls = UserSubscribes.objects.filter()
        noties = Notifications.objects.filter()

        data = {
            'title': title,
            'users': users,
            'saved_urls': saved_urls,
            'seen_urls': seen_urls,
            'subscribed_urls': subscribed_urls,
            'noties': noties,
        }
        return data
