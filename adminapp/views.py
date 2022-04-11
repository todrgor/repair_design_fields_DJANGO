from publicationapp.models import *
from authapp.models import *

from .forms import *
from django.shortcuts import render
from authapp.models import *
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.utils import timezone
# from datetime import datetime
from django.core.files.storage import FileSystemStorage

# получение жалобы на пользователя или публикацию через ajax
@csrf_exempt
def NewComplaint(request):
    if request.user.is_authenticated:
        if request.is_ajax():
            complaint = request.POST
            contacting_support = None
            # print(str(request.POST))
            # print(str(request.FILES))

            # если обращение -- жалоба на публикацию
            if int(complaint['complaint_type']) == 11:
                # print(complaint['complaint_id'])
                # print(complaint['complaint_type'])
                # print(isinstance(int(complaint['complaint_type']), int))
                # print(complaint['complaint_text'])

                pub_complaint = Publication.objects.get(id=complaint['complaint_id'])
                pub_complaint.reported_count +=1
                pub_complaint.save()
                contacting_support = ContactingSupport.objects.create(title=('Жалоба на публикацию «' + pub_complaint.title +'»'), role=ContactingSupportTypes.objects.get(id=11), asked_by=request.user, ask_content=complaint['complaint_text'], ask_additional_info=complaint['complaint_id'], when_asked=timezone.now())

                noti=Publication.objects.create(title=('Ваша жалоба на публикацию «'+ pub_complaint.title +'» принята!'), role=PubRoles.objects.get(id=51), preview=(pub_complaint.preview.name), content_first_desc="Ждите результата здесь, в уведомлениях", content_last_desc='', author=request.user)
                Notifications.objects.create(user_receiver=request.user, noti_for_user=noti)
                noti=Publication.objects.create(title=('На Вашу публикацию «'+ pub_complaint.title +'» поступила 1 новая жалоба.'), role=PubRoles.objects.get(id=51), preview=(pub_complaint.preview.name), content_first_desc="Ждите результата здесь, в уведомлениях", content_last_desc='', author=request.user)
                Notifications.objects.create(user_receiver=pub_complaint.author, noti_for_user=noti)

            # если обращение -- жалоба на пользователя
            if int(complaint['complaint_type']) == 12:
                user_complaint = User.objects.get(id=complaint['complaint_id'])
                user_complaint.reported_count +=1
                user_complaint.save()
                contacting_support = ContactingSupport.objects.create(title=('Жалоба на пользователя «' + user_complaint.username +'»'), role=ContactingSupportTypes.objects.get(id=12), asked_by=request.user, ask_content=complaint['complaint_text'], ask_additional_info=complaint['complaint_id'], when_asked=timezone.now())

                noti=Publication.objects.create(title=('Ваша жалоба на пользователя «'+ user_complaint.username +'» принята!'), role=PubRoles.objects.get(id=51), preview=(user_complaint.photo.name), content_first_desc="Ждите результата здесь, в уведомлениях", content_last_desc='', author=request.user)
                Notifications.objects.create(user_receiver=request.user, noti_for_user=noti)
                noti=Publication.objects.create(title=('На Ваш профиль поступила 1 новая жалоба.'), role=PubRoles.objects.get(id=51), preview=(user_complaint.photo.name), content_first_desc="Ждите результата здесь, в уведомлениях", content_last_desc='', author=request.user)
                Notifications.objects.create(user_receiver=user_complaint, noti_for_user=noti)

            # если обращение поступило вместе с фотками
            if request.FILES and int(complaint['complaint_type']) in [11, 12]:
                fs = FileSystemStorage()
                for one_photo in request.FILES:
                    # print(photo)
                    fs.save(('contacting_support_media/' + one_photo), request.FILES[one_photo])
                    ContactingSupportPhotos.objects.create(contacting_support_action=contacting_support, photo=('contacting_support_media/' + one_photo))

            if int(complaint['complaint_type']) in [11, 12]:
                return JsonResponse({'result': True})


# все обращения в поддержку:
# их вывод и обработка администраторами
def LettersToSupport(request):
    if request.user.is_authenticated:
        if request.user.role.id in [3, 4]:
            answer_form = AnswerForm()
            answer_to_report_form = AnswerToReportForm()
            if request.method == 'POST':
                if not request.POST['answer'].isspace():
                    answer = request.POST
                    letter = ContactingSupport.objects.get(id=int(answer['ask_id']))
                    # у меня проблема: при перезагрзке страницы request.POST полностью сохраняется,
                    # из-за этого те же самые изменения создаются второй раз. единственное найденное
                    # решение, которое очень похоже на кастыль -- проверять, есть ли уже в БД ответ
                    # на это обрщание. рабоатает. но request.POST по-прежнему повторяется
                    if not letter.answer_content:
                        letter_type = letter.role.id

                        if letter_type in [21, 22, 31, 32]:
                            letter.answer_content = answer['answer']
                            letter.answered_by = request.user
                            letter.when_answered = timezone.now()

                            if letter_type in [21, 22]:
                                if letter_type == 21:
                                    role_name = 'роль автора'
                                    role_id = 2
                                if letter_type == 22:
                                    role_name = 'роль админа'
                                    role_id = 3
                                if answer['change_role'] == 'Назначить новую роль':
                                    decision = 'поздравляем! Теперь у Вас '+ role_name +'!'
                                    letter.answer_additional_info = 1
                                    letter_author = letter.asked_by
                                    letter_author.role = UserRoles.objects.get(id=role_id)
                                    letter_author.save()
                                else:
                                    decision = 'к сожалению, '+ role_name +' Вам не назначена.'
                                    letter.answer_additional_info = 0
                                noti=Publication.objects.create(title=('Ваша заявка на '+ role_name +' была рассмотрена. Решение: '+ decision +' Также ответ от поддержки: ' + answer['answer']), role=PubRoles.objects.get(id=51), preview=(letter.asked_by.photo.name), content_first_desc="Пишите ещё, если что-то непонятно, или у Вас родилась идея!", content_last_desc='', author=request.user)
                            if letter_type == 31:
                                noti=Publication.objects.create(title=('Ваш вопрос был рассмотрен. Ответ от поддержки: ' + answer['answer']), role=PubRoles.objects.get(id=51), preview=(letter.asked_by.photo.name), content_first_desc="Пишите ещё, если что-то непонятно, или у Вас родилась идея!", content_last_desc='', author=request.user)
                            if letter_type == 32:
                                noti=Publication.objects.create(title=('Спасибо Вам за Вашу идею! Идея была рассмотрена.  Ответ от поддержки: ' + answer['answer']), role=PubRoles.objects.get(id=51), preview=(letter.asked_by.photo.name), content_first_desc="Ждём ещё идей!", content_last_desc='', author=request.user)
                            Notifications.objects.create(user_receiver=letter.asked_by, noti_for_user=noti)

                        letter.save()
                        print(str(answer))
                else:
                    answer_form = AnswerForm({'answer': None})
                    answer_to_report_form = AnswerToReportForm({'answer': None, 'decision': 'just_answer'})


            ideas = ContactingSupport.objects.filter(role=32).exclude(answer_content=None)
            new_ideas = ContactingSupport.objects.filter(role=32, answer_content=None)
            new_ideas_count = new_ideas.count()
            all_ideas_photos = ContactingSupportPhotos.objects.filter(contacting_support_action__role=32)

            questions = ContactingSupport.objects.filter(role=31).exclude(answer_content=None)
            new_questions = ContactingSupport.objects.filter(role=31, answer_content=None)
            new_questions_count = new_questions.count()
            all_questions_photos = ContactingSupportPhotos.objects.filter(contacting_support_action__role=31)

            applications = ContactingSupport.objects.filter(role__in=[21, 22]).exclude(answer_content=None)
            new_applications = ContactingSupport.objects.filter(role__in=[21, 22], answer_content=None)
            new_applications_count = new_applications.count()
            all_applications_photos = ContactingSupportPhotos.objects.filter(contacting_support_action__role__in=[21, 22])

            reports = ContactingSupport.objects.filter(role__in=[11, 12]).exclude(answer_content=None)
            new_reports = ContactingSupport.objects.filter(role__in=[11, 12], answer_content=None)
            new_reports_count = new_reports.count()
            all_reports_photos = ContactingSupportPhotos.objects.filter(contacting_support_action__role__in=[11, 12])
            reported_pubs_list_id = [p.ask_additional_info for p in ContactingSupport.objects.filter(role=11)]
            reported_users_list_id = [u.ask_additional_info for u in ContactingSupport.objects.filter(role=12)]
            reported_pubs = Publication.objects.filter(id__in=reported_pubs_list_id)
            reported_users = User.objects.filter(id__in=reported_users_list_id)

            strange_letters = ContactingSupport.objects.filter(role=0).exclude(answer_content=None)
            new_strange_letters = ContactingSupport.objects.filter(role=0, answer_content=None)
            new_strange_letters_count = new_strange_letters.count()
            all_strange_letters_photos = ContactingSupportPhotos.objects.filter(contacting_support_action__role=0)

            # print(ideas)
            # print(new_ideas)
            # print(questions)
            # print(new_questions)
            # print(applications)
            # print(new_applications)
            # print(reports)
            # print(reported_pubs_list_id)
            # print(reported_pubs)
            # print(isinstance(1,str))
            # print(strange_letters)
            # print(new_strange_letters)

            title = 'Обращения в поддержку'
            if new_ideas or new_questions or new_applications or new_reports or new_strange_letters:
                title = str(new_ideas_count + new_questions_count + new_applications_count + new_reports_count + new_strange_letters_count) + ' обращений ждут ответа | Обращения в поддержку'
            content = {
                'answer_form': answer_form,
                'answer_to_report_form': answer_to_report_form,

                'ideas': ideas,
                'new_ideas': new_ideas,
                'new_ideas_count': new_ideas_count,
                'all_ideas_photos': all_ideas_photos,

                'questions': questions,
                'new_questions': new_questions,
                'new_questions_count': new_questions_count,
                'all_questions_photos': all_questions_photos,

                'applications': applications,
                'new_applications': new_applications,
                'new_applications_count': new_applications_count,
                'all_applications_photos': all_applications_photos,

                'reports': reports,
                'new_reports': new_reports,
                'new_reports_count': new_reports_count,
                'all_reports_photos': all_reports_photos,
                'reported_pubs': reported_pubs,
                'reported_users': reported_users,

                'strange_letters': strange_letters,
                'new_strange_letters': new_strange_letters,
                'new_strange_letters_count': new_strange_letters_count,
                'all_strange_letters_photos': all_strange_letters_photos,

                'title': title,
            }
            return render(request, 'adminapp/letters_to_support.html', content)
        else:
            return HttpResponse("Простите, но у Вас недостаточно прав для этой страницы. ")
    else:
        return HttpResponse("Сначала авторизируйтесь!")


# стартовая страница админа
class StartPanel(ListView):
    model =  Publication
    template_name = 'adminapp/main.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated or not self.request.user.role.id in [3, 4]:
            print('проникновение туда, куда нельзя')
            return HttpResponse("Простите, но у Вас недостаточно прав для этой страницы. ")

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


# страница всех публикаций в ИС
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


# страница всех пользователей в ИС
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
