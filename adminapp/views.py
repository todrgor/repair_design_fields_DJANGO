from django.shortcuts import render
from authapp.models import *
from publicationapp.models import *
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.utils import timezone
# from datetime import datetime


@csrf_exempt
def NewComplaint(request):
    if request.user.is_authenticated:
        if request.is_ajax():
            complaint = request.POST

            # если обращение -- жалоба на публикацию
            if int(complaint['complaint_type']) == 11:
                # print(complaint['complaint_id'])
                # print(complaint['complaint_type'])
                # print(isinstance(int(complaint['complaint_type']), int))
                # print(complaint['complaint_text'])

                pub_complaint = Publication.objects.get(id=complaint['complaint_id'])
                pub_complaint.reported_count +=1
                pub_complaint.save()
                ContactingSupport.objects.create(title=('Жалоба на публикацию «' + pub_complaint.title +'»'), role=ContactingSupportTypes.objects.get(id=11), asked_by=request.user, ask_content=complaint['complaint_text'], ask_additional_info=complaint['complaint_id'], when_asked=timezone.now())

                noti=Publication.objects.create(title=('Ваша жалоба на публикацию «'+ pub_complaint.title +'» принята!'), role=PubRoles.objects.get(id=51), preview=(pub_complaint.preview.name), content_first_desc="Ждите результата здесь, в уведомлениях", content_last_desc='', author=request.user)
                Notifications.objects.create(user_receiver=request.user, noti_for_user=noti)
                noti=Publication.objects.create(title=('На Вашу публикацию «'+ pub_complaint.title +'» поступила 1 новая жалоба.'), role=PubRoles.objects.get(id=51), preview=(pub_complaint.preview.name), content_first_desc="Ждите результата здесь, в уведомлениях", content_last_desc='', author=request.user)
                Notifications.objects.create(user_receiver=pub_complaint.author, noti_for_user=noti)
                return JsonResponse({'result': True})

            # если обращение -- жалоба на публикацию
            if int(complaint['complaint_type']) == 12:
                user_complaint = User.objects.get(id=complaint['complaint_id'])
                user_complaint.reported_count +=1
                user_complaint.save()
                ContactingSupport.objects.create(title=('Жалоба на пользователя «' + user_complaint.username +'»'), role=ContactingSupportTypes.objects.get(id=12), asked_by=request.user, ask_content=complaint['complaint_text'], ask_additional_info=complaint['complaint_id'], when_asked=timezone.now())

                noti=Publication.objects.create(title=('Ваша жалоба на пользователя «'+ user_complaint.username +'» принята!'), role=PubRoles.objects.get(id=51), preview=(user_complaint.photo.name), content_first_desc="Ждите результата здесь, в уведомлениях", content_last_desc='', author=request.user)
                Notifications.objects.create(user_receiver=request.user, noti_for_user=noti)
                noti=Publication.objects.create(title=('На Ваш профиль поступила 1 новая жалоба.'), role=PubRoles.objects.get(id=51), preview=(user_complaint.photo.name), content_first_desc="Ждите результата здесь, в уведомлениях", content_last_desc='', author=request.user)
                Notifications.objects.create(user_receiver=user_complaint, noti_for_user=noti)
                return JsonResponse({'result': True})


class StartPanel(ListView):
    model =  Publication
    template_name = 'adminapp/main.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated or not self.request.user.role.id in [3, 4]:
            print('проникновение туда, куда нельзя')
            return HttpResponse("Простите, но у Вас недостаточно прав для этой страницы. ")
            # return HttpResponseRedirect('/')
        else:
            resp = super().get(*args, **kwargs)
            print('Finished processing GET request')
            print(str(resp))
            return resp

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
        if not self.request.user.is_authenticated or not self.request.user.role.id in [3, 4]:
            print('проникновение туда, куда нельзя')
            return HttpResponse("Простите, но у Вас недостаточно прав для этой страницы. ")
            # return HttpResponseRedirect('/')
        else:
            resp = super().get(*args, **kwargs)
            print('Finished processing GET request')
            print(str(resp))
            return resp

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
        if not self.request.user.is_authenticated or not self.request.user.role.id in [3, 4]:
            print('проникновение туда, куда нельзя')
            return HttpResponse("Простите, но у Вас недостаточно прав для этой страницы. ")
            # return HttpResponseRedirect('/')
        else:
            resp = super().get(*args, **kwargs)
            print('Finished processing GET request')
            print(str(resp))
            return resp

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
