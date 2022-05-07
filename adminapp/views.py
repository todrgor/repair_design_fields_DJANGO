from publicationapp.models import *
from authapp.models import *

from .forms import *
from django.shortcuts import render
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.utils.formats import localize
# from datetime import datetime
from django.core.files.storage import FileSystemStorage

#   получение жалобы на пользователя или публикацию через ajax
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
                contacting_support = ContactingSupport.objects.create(title=('Жалоба на публикацию «' + pub_complaint.title +'»'), type=ContactingSupportTypes.objects.get(id=11), asked_by=request.user, ask_content=complaint['complaint_text'], ask_additional_info=complaint['complaint_id'], when_asked=timezone.now())

                noti=Publication.objects.create(title=('Ваша жалоба на публикацию «'+ pub_complaint.title +'» принята!'), type=PubTypes.objects.get(id=51), preview=(pub_complaint.preview.name), content_first_desc="Ждите результата здесь, в уведомлениях", content_last_desc='', author=request.user)
                Notifications.objects.create(user_receiver=request.user, noti_for_user=noti)
                noti=Publication.objects.create(title=('На Вашу публикацию «'+ pub_complaint.title +'» поступила 1 новая жалоба.'), type=PubTypes.objects.get(id=51), preview=(pub_complaint.preview.name), content_first_desc="Ждите результата здесь, в уведомлениях", content_last_desc='', author=request.user)
                Notifications.objects.create(user_receiver=pub_complaint.author, noti_for_user=noti)

            # если обращение -- жалоба на пользователя
            if int(complaint['complaint_type']) == 12:
                user_complaint = User.objects.get(id=complaint['complaint_id'])
                user_complaint.reported_count +=1
                user_complaint.save()
                contacting_support = ContactingSupport.objects.create(title=('Жалоба на пользователя «' + user_complaint.username +'»'), type=ContactingSupportTypes.objects.get(id=12), asked_by=request.user, ask_content=complaint['complaint_text'], ask_additional_info=complaint['complaint_id'], when_asked=timezone.now())

                noti=Publication.objects.create(title=('Ваша жалоба на пользователя «'+ user_complaint.username +'» принята!'), type=PubTypes.objects.get(id=51), preview=(user_complaint.photo.name), content_first_desc="Ждите результата здесь, в уведомлениях", content_last_desc='', author=request.user)
                Notifications.objects.create(user_receiver=request.user, noti_for_user=noti)
                noti=Publication.objects.create(title=('На Ваш профиль поступила 1 новая жалоба.'), type=PubTypes.objects.get(id=51), preview=(user_complaint.photo.name), content_first_desc="Ждите результата здесь, в уведомлениях", content_last_desc='', author=request.user)
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


#   все обращения в поддержку:
#   их вывод и обработка администраторами
def LettersToSupport(request):
    if request.user.is_authenticated:
        if request.user.role.id in [3, 4]:
            answer_form = AnswerForm()
            answer_to_report_form = AnswerToReportForm()
            if request.method == 'POST' and ContactingSupport.objects.filter(id=int(request.POST['ask_id'])).count() >0:
                if not request.POST['answer'].isspace():
                    answer = request.POST
                    letter = ContactingSupport.objects.get(id=int(answer['ask_id']))
                    # у меня проблема: при перезагрзке страницы request.POST полностью сохраняется,
                    # из-за этого те же самые изменения создаются второй раз. единственное найденное
                    # решение, которое очень похоже на кастыль -- проверять, есть ли уже в БД ответ
                    # на это обрщание. рабоатает. но request.POST по-прежнему повторяется
                    if letter.type.id == 0 and 'delete_letter' in answer:
                        noti=Publication.objects.create(title=('Спасибо Вам за Ваше обращение! С Ваши обращением «' + letter.title + '», отправленным ' + str(localize(letter.when_asked)) + ', на каком-то этапе обработки что-то пошло не так... Оно было удалено. Если вопрос остаётся открытым, пожалуйста, сделайте обращение в поддержку ешё. Также: если что, на обращение был сделан ответ: «' + answer['answer'] + '». С заботой, Ваша поддержка «Ремонта и дизайна»'), type=PubTypes.objects.get(id=51), preview=letter.asked_by.photo.name, content_first_desc="Просим прощения за неудобства ❤", content_last_desc='', author=request.user)
                        Notifications.objects.create(user_receiver=letter.asked_by, noti_for_user=noti)
                        if not letter.answer_content:
                            letter.answer_content = answer['answer']
                            letter.answered_by = request.user
                            letter.when_answered = timezone.now()
                        letter.delete()

                    if not letter.answer_content:
                        letter_type = letter.type.id

                        if letter_type in [11, 12, 21, 22, 31, 32]:
                            letter.answer_content = answer['answer']
                            letter.answered_by = request.user
                            letter.when_answered = timezone.now()

                            if letter_type in [11, 12]:
                                letter.answer_additional_info = 0
                                if letter_type == 11:
                                    pub = Publication.objects.get(id = letter.ask_additional_info)
                                    noti_preview = pub.preview.name
                                    report_reason_receiver = pub.author
                                if letter_type == 12:
                                    user = User.objects.get(id = letter.ask_additional_info)
                                    noti_preview = user.photo.name
                                    report_reason_receiver = user

                                if (not 'is_delete_pub' in answer and not 'is_deny_rules' in answer and not 'is_delete_account' in answer) or (letter_type == 11 and Publication.objects.get(id=letter.ask_additional_info).author.role.id == 4) or (letter_type == 12 and User.objects.get(id=letter.ask_additional_info).role.id == 4):
                                    # print('ответ только сообщением')
                                    noti=Publication.objects.create(title=('Спасибо Вам за Вашу бдительность и Вашу жалобу! ' + letter.title + ', отправленная Вами ' + str(localize(letter.when_asked)) + ', была рассмотрена.  Решение поддержки – закрыть вопрос только текстовым ответом: «' + answer['answer'] + '». Если решение не устраивает и/или не решает вопроса, подайте жалобу ещё раз, упомянув об этом. С заботой, Ваша поддержка «Ремонта и дизайна»'), type=PubTypes.objects.get(id=51), preview=noti_preview, content_first_desc="Если решение не устраивает, можно подать жалобу ещё раз ❤", content_last_desc='', author=request.user)
                                    Notifications.objects.create(user_receiver=letter.asked_by, noti_for_user=noti)
                                    noti=Publication.objects.create(title=(letter.title + ', отправленная пользователем «' + letter.asked_by.username + '» ' + str(localize(letter.when_asked)) + ', была рассмотрена.  Решение поддержки – закрыть вопрос только текстовым ответом: «' + answer['answer'] + '». Если решение не устраивает и/или не решает вопроса, подайте жалобу, упомянув об этом. С заботой, Ваша поддержка «Ремонта и дизайна»'), type=PubTypes.objects.get(id=51), preview=noti_preview, content_first_desc="Если решение не устраивает, можно подать жалобу ❤", content_last_desc='', author=request.user)
                                    Notifications.objects.create(user_receiver=report_reason_receiver, noti_for_user=noti)

                                else:
                                    # print('ответ не только сообщением')
                                    decision = ''
                                    decision_for_report_reason_receiver = ''
                                    if letter_type == 11 and 'is_delete_pub' in answer:
                                        # print('+ удалить публикацию')
                                        decision = 'безвозвратно удалить публикацию «' + pub.title + '»'
                                        pub.delete()
                                        letter.answer_additional_info += 10

                                    if 'is_deny_rules' in answer and not 'is_delete_account' in answer:
                                        # print('+ лишить роли')
                                        if not decision or not decision.isspace():
                                            decision += ' и '
                                            decision_for_report_reason_receiver = decision
                                        decision += 'понизить пользователя «' + report_reason_receiver.username + '» до роли "Пользователь-зритель"'
                                        decision_for_report_reason_receiver += 'понизить Вас до роли "Пользователь-зритель"'
                                        report_reason_receiver.role = UserRoles.objects.get(id=1)
                                        report_reason_receiver.save()
                                        letter.answer_additional_info += 100

                                    if 'is_delete_account' in answer:
                                        # print('+ удалить аккаунт')
                                        if not decision or not decision.isspace():
                                            decision += ' и '
                                        decision += 'безвозвратно удалить пользователя «' + report_reason_receiver.username + '»'
                                        report_reason_receiver.delete()
                                        letter.answer_additional_info += 1000
                                    else:
                                        noti=Publication.objects.create(title=(letter.title + ', отправленная пользователем «' + letter.asked_by.username + '» ' + str(localize(letter.when_asked)) + ', была рассмотрена.  Решение поддержки – ' + decision_for_report_reason_receiver + '. Также ответ от поддержки: «' + answer['answer'] + '». Если решение не устраивает и/или не решает вопроса, подайте жалобу, упомянув об этом. С заботой, Ваша поддержка «Ремонта и дизайна»'), type=PubTypes.objects.get(id=51), preview=noti_preview, content_first_desc="Если решение не устраивает, можно подать жалобу ❤", content_last_desc='', author=request.user)
                                        Notifications.objects.create(user_receiver=report_reason_receiver, noti_for_user=noti)
                                    noti=Publication.objects.create(title=('Спасибо Вам за Вашу бдительность и Вашу жалобу! ' + letter.title + ', отправленная Вами ' + str(localize(letter.when_asked)) + ', была рассмотрена.  Решение поддержки – ' + decision + '. Также ответ от поддержки: «' + answer['answer'] + '». Если решение не устраивает и/или не решает вопроса, подайте жалобу ещё раз, упомянув об этом. С заботой, Ваша поддержка «Ремонта и дизайна»'), type=PubTypes.objects.get(id=51), preview=noti_preview, content_first_desc="Если решение не устраивает, можно подать жалобу ещё раз ❤", content_last_desc='', author=request.user)
                                    Notifications.objects.create(user_receiver=letter.asked_by, noti_for_user=noti)
                                # print('report of type', letter_type)

                            if letter_type in [21, 22]:
                                letter.ask_additional_info = 999
                                if letter_type == 21:
                                    role_name = 'роль автора'
                                    role_id = 2
                                if letter_type == 22:
                                    role_name = 'роль админа'
                                    role_id = 3

                                if letter.asked_by.role.id == 4 and User.objects.filter(role=UserRoles.objects.get(id=4)).count() <= 1:
                                    noti=Publication.objects.create(title=('Ваша заявка на '+ role_name +' была рассмотрена. На данный момент в системе всего 1 суперпользователь, поэтому нам опасно менять Вам роль. Найдите наследника и обращайтесь ещё! Также ответ от поддержки: «' + answer['answer'] +'». С заботой, Ваша поддержка «Ремонта и дизайна»'), type=PubTypes.objects.get(id=51), preview=(letter.asked_by.photo.name), content_first_desc="По-другому пока не можем. Просим простить нас ❤", content_last_desc='', author=request.user)
                                    Notifications.objects.create(user_receiver=letter.asked_by, noti_for_user=noti)
                                    noti=Publication.objects.create(title=('Заявка на '+ role_name +' от пользователя «' + letter.asked_by.username + '» никак не может быть одобрена: на данный момент в системе всего 1 суперпользователь, поэтому опасно менять ему роль. Придётся подождать наследника и обратиться потом ещё. С заботой, Ваша поддержка «Ремонта и дизайна»'), type=PubTypes.objects.get(id=51), preview=(letter.asked_by.photo.name), content_first_desc="По-другому мы пока не можем. вот так вот ❤", content_last_desc='', author=request.user)
                                    Notifications.objects.create(user_receiver=request.user, noti_for_user=noti)

                                else:
                                    if answer['change_role'] == 'Назначить новую роль':
                                        decision = 'поздравляем! Теперь у Вас '+ role_name +'!'
                                        letter.answer_additional_info = 1
                                        letter_author = letter.asked_by
                                        letter_author.role = UserRoles.objects.get(id=role_id)
                                        letter_author.save()
                                    else:
                                        decision = 'к сожалению, '+ role_name +' Вам не назначена.'
                                        letter.answer_additional_info = 0
                                    noti=Publication.objects.create(title=('Ваша заявка на '+ role_name +' была рассмотрена. Решение: '+ decision +' Также ответ от поддержки: «' + answer['answer'] +'». С заботой, Ваша поддержка «Ремонта и дизайна»'), type=PubTypes.objects.get(id=51), preview=(letter.asked_by.photo.name), content_first_desc="Пишите ещё, если что-то непонятно, или у Вас родилась идея! ❤", content_last_desc='', author=request.user)
                                    Notifications.objects.create(user_receiver=letter.asked_by, noti_for_user=noti)

                            if letter_type in [31, 32]:
                                if letter_type == 31:
                                    noti=Publication.objects.create(title=('Ваш вопрос был рассмотрен. Ответ от поддержки: «' + answer['answer'] + '».'), type=PubTypes.objects.get(id=51), preview=(letter.asked_by.photo.name), content_first_desc="Пишите ещё, если что-то непонятно, или у Вас родилась идея! ❤", content_last_desc='', author=request.user)
                                if letter_type == 32:
                                    noti=Publication.objects.create(title=('Спасибо Вам за Вашу идею! Идея была рассмотрена.  Ответ от поддержки: «' + answer['answer'] + '». С заботой, Ваша поддержка «Ремонта и дизайна»'), type=PubTypes.objects.get(id=51), preview=(letter.asked_by.photo.name), content_first_desc="Ждём ещё идей! ❤", content_last_desc='', author=request.user)
                                Notifications.objects.create(user_receiver=letter.asked_by, noti_for_user=noti)

                        # if letter_type in [11, 12]:
                        #     if ('is_just_answer' in answer) or (letter_type == 11 and Publication.objects.get(id=letter.ask_additional_info).author.role.id == 4) or (letter_type == 12 and User.objects.get(id=letter.ask_additional_info).role.id == 4):
                        #         print('ответ только сообщением')
                        #     else:
                        #         print('ответ не только сообщением')
                        #         if letter_type == 11 and 'is_delete_pub' in answer:
                        #             print('+ удалить публикацию')
                        #         if 'is_deny_rules' in answer:
                        #             print('+ лишить роли')
                        #         if 'is_delete_account' in answer:
                        #             print('+ удалить аккаунт')
                        #     print('report of type', letter_type)

                        letter.save()
                        print(str(answer))
                        # print(str(answer.is_delete_pub))
                        # print(str(answer.is_deny_rules))
                        # print(str(answer.is_delete_account))
                else:
                    answer_form = AnswerForm({'answer': None})
                    answer_to_report_form = AnswerToReportForm({'answer': None, 'decision': 'just_answer'})


            ideas = ContactingSupport.objects.filter(type=32).exclude(answer_content=None)
            new_ideas = ContactingSupport.objects.filter(type=32, answer_content=None)
            new_ideas_count = new_ideas.count()
            all_ideas_photos = ContactingSupportPhotos.objects.filter(contacting_support_action__type=32)

            questions = ContactingSupport.objects.filter(type=31).exclude(answer_content=None)
            new_questions = ContactingSupport.objects.filter(type=31, answer_content=None)
            new_questions_count = new_questions.count()
            all_questions_photos = ContactingSupportPhotos.objects.filter(contacting_support_action__type=31)

            applications = ContactingSupport.objects.filter(type__in=[21, 22]).exclude(answer_content=None)
            new_applications = ContactingSupport.objects.filter(type__in=[21, 22], answer_content=None)
            new_applications_count = new_applications.count()
            all_applications_photos = ContactingSupportPhotos.objects.filter(contacting_support_action__type__in=[21, 22])

            reports = ContactingSupport.objects.filter(type__in=[11, 12]).exclude(answer_content=None)
            new_reports = ContactingSupport.objects.filter(type__in=[11, 12], answer_content=None)
            new_reports_count = new_reports.count()
            all_reports_photos = ContactingSupportPhotos.objects.filter(contacting_support_action__type__in=[11, 12])
            reported_pubs_list_id = [p.ask_additional_info for p in ContactingSupport.objects.filter(type=11)]
            reported_users_list_id = [u.ask_additional_info for u in ContactingSupport.objects.filter(type=12)]
            reported_pubs = Publication.objects.filter(id__in=reported_pubs_list_id)
            reported_users = User.objects.filter(id__in=reported_users_list_id)

            strange_letters = ContactingSupport.objects.filter(type=0).exclude(answer_content=None)
            new_strange_letters = ContactingSupport.objects.filter(type=0, answer_content=None)
            new_strange_letters_count = new_strange_letters.count()
            all_strange_letters_photos = ContactingSupportPhotos.objects.filter(contacting_support_action__type=0)

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
            return HttpResponse("Простите, но у Вас недостаточно прав для этой страницы. <a href='/'>На главную</a>")
    else:
        return HttpResponse("Сначала авторизируйтесь! <a href='/login/'>Авторизоваться</a>")


#    отображение, создание,
#    редактирование и удаление тегов и их категорий
@csrf_exempt
def TagsAndTagCategories(request):
    if request.user.is_authenticated:
        if request.user.role.id in [4]:
            if request.method == 'POST':
                method_POST = request.POST

                if (
                    'to_create_or_edit' in method_POST and 'tag_or_category_to_create_or_edit' in method_POST and 'category_or_tag_name' in method_POST
                    and method_POST['to_create_or_edit'] and method_POST['tag_or_category_to_create_or_edit'] and method_POST['category_or_tag_name']
                    ):

                    if method_POST['tag_or_category_to_create_or_edit'] == 'category':
                        object = None
                        if method_POST['to_create_or_edit'] == 'create' and not TagCategory.objects.filter(name=method_POST['category_or_tag_name']):
                            object = TagCategory.objects.create(name=method_POST['category_or_tag_name'])
                            object_type = 'создана категория «'+ object.name +'»'
                        if method_POST['to_create_or_edit'] == 'edit' and 'object_id' in method_POST and method_POST['object_id'] and TagCategory.objects.filter(id=method_POST['object_id']):
                            object = TagCategory.objects.get(id=method_POST['object_id'])
                            if object.name != method_POST['category_or_tag_name']:
                                object.name = method_POST['category_or_tag_name']
                                object.save()
                                object_type = 'изменена категория «'+ object.name +'»'
                        if object:
                            noti=Publication.objects.create(title=('Успешно '+ object_type +'!'), type=PubTypes.objects.get(id=51), preview=(request.user.photo.name), content_first_desc="Наверное умничкааа) А других уведомить и желательно ещё причину и возможности указать? А?", content_last_desc='', author=request.user)
                            Notifications.objects.create(user_receiver=request.user, noti_for_user=noti)


                    if method_POST['tag_or_category_to_create_or_edit'] == 'tag':
                        selected_pub_types = [method_POST[item] for item in method_POST.keys() if 'pub_type_' in item]
                        object = None
                        if method_POST['to_create_or_edit'] == 'create' and 'category' in method_POST and selected_pub_types and method_POST['category'] and not Tag.objects.filter(name=method_POST['category_or_tag_name'], category=method_POST['category']):
                            object = Tag.objects.create(name=method_POST['category_or_tag_name'], category=TagCategory.objects.get(id=method_POST['category']))
                            object.pub_type.set(PubTypes.objects.filter(id__in=selected_pub_types))
                            object.save()
                            object_type = 'создан тег «'+ object.name +'»'
                        if method_POST['to_create_or_edit'] == 'edit' and 'object_id' in method_POST and method_POST['object_id'] and 'category' in method_POST and selected_pub_types and method_POST['category'] and Tag.objects.filter(id=method_POST['object_id']):
                            object = Tag.objects.get(id=method_POST['object_id'])
                            if object.name != method_POST['category_or_tag_name'] or object.category.id != int(method_POST['category']) or set(object.pub_type.all()) != set(PubTypes.objects.filter(id__in=selected_pub_types)):
                                object.name = method_POST['category_or_tag_name']
                                object.category = TagCategory.objects.get(id=method_POST['category'])
                                object.pub_type.set(PubTypes.objects.filter(id__in=selected_pub_types))
                                object.save()
                                object_type = 'изменён тег «'+ object.name +'»'
                        if object:
                            noti=Publication.objects.create(title=('Успешно '+ object_type +'!'), type=PubTypes.objects.get(id=51), preview=(request.user.photo.name), content_first_desc="Наверное умничкааа) А других уведомить и желательно ещё причину и возможности указать? А?", content_last_desc='', author=request.user)
                            Notifications.objects.create(user_receiver=request.user, noti_for_user=noti)

                if 'tag_or_category_to_delete' in method_POST and 'object_id' in method_POST and method_POST['tag_or_category_to_delete'] and method_POST['object_id']:
                    if method_POST['tag_or_category_to_delete'] == 'category':
                        object = TagCategory.objects.filter(id=method_POST['object_id'])
                        if object:
                            object = TagCategory.objects.get(id=method_POST['object_id'])
                            object_type = 'удалена категория «'+ object.name +'»'
                    if method_POST['tag_or_category_to_delete'] == 'tag':
                        object = Tag.objects.filter(id=method_POST['object_id'])
                        if object:
                            object = Tag.objects.get(id=method_POST['object_id'])
                            object_type = 'удалён тег «'+ object.name +'»'
                    if object:
                        noti=Publication.objects.create(title=('Успешно '+ object_type +'!'), type=PubTypes.objects.get(id=51), preview=(request.user.photo.name), content_first_desc="Ну и зачем? А других уведомить и желательно ещё причину указать? А?", content_last_desc='', author=request.user)
                        Notifications.objects.create(user_receiver=request.user, noti_for_user=noti)
                        object.delete()

            title = 'Теги публикаций и их категории'
            tags = Tag.objects.all()
            tag_categories = TagCategory.objects.all()
            pubs = Publication.objects.filter(type__in=[11, 21, 31])
            pub_types = PubTypes.objects.filter(id__in=[11, 21, 31])

            content = {
                'title': title,
                'tags': tags,
                'tag_categories': tag_categories,
                'pubs': pubs,
                'pub_types': pub_types,
            }
            return render(request, 'adminapp/tags_and_tag_categories.html', content)
        else:
            return HttpResponse("Простите, но у Вас недостаточно прав для этой страницы. <a href='/'>На главную</a>")
    else:
        return HttpResponse("Сначала авторизируйтесь! <a href='/login/'>Авторизоваться</a>")

#   стартовая страница админа
class StartPanel(ListView):
    model =  Publication
    template_name = 'adminapp/main.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated or not self.request.user.role.id in [3, 4]:
            print('проникновение туда, куда нельзя')
            return HttpResponse("Простите, но у Вас недостаточно прав для этой страницы. <a href='/'>На главную</a>")
        else:
            resp = super().get(*args, **kwargs)
            print('Finished processing GET request')
            print(str(resp))
            return resp

    def get_context_data(self, **kwargs):
        title ='Главная | Панель администратора'
        pubs = Publication.objects.filter(type__id__in=[11, 21, 31]).order_by('-pushed')[:3]
        noties = Notifications.objects.filter().order_by('-when')[:4]
        users = User.objects.filter().order_by('-last_entry')[:4]
        # applications =
        # complaints =
        tag_categories = TagCategory.objects.all().order_by('id')[:4]
        tags = [Tag.objects.filter(category=category).exclude(name='Авторский стиль (как видит сам автор, без придуманных стилей)')[:4] for category in tag_categories]
        new_letters_to_support = ContactingSupport.objects.filter(answer_content=None).order_by('-when_asked')[:5]
        answered_letters_to_support = ContactingSupport.objects.exclude(answer_content=None).order_by('-when_asked')[:3] if not new_letters_to_support else None

        data = {
            # 'noties': noties,
            'title': title,
            'pubs': pubs,
            'users': users,
            'new_letters_to_support': new_letters_to_support,
            'answered_letters_to_support': answered_letters_to_support,
    		'tags': tags,
    		'tag_categories': tag_categories,
        }
        return data


#   страница всех публикаций в ИС
class PubList(ListView):
    model =  Publication
    template_name = 'adminapp/publications.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated or not self.request.user.role.id in [3, 4]:
            print('проникновение туда, куда нельзя')
            return HttpResponse("Простите, но у Вас недостаточно прав для этой страницы. <a href='/'>На главную</a>")
            # return HttpResponseRedirect('/')
        else:
            resp = super().get(*args, **kwargs)
            print('Finished processing GET request')
            print(str(resp))
            return resp

    def get_context_data(self, *, object_list=None, **kwargs):
        title ='Публикации | Панель администратора'
        pubs = Publication.objects.filter(type__id__in=[11, 21, 31])
        saved_urls = SavedPubs.objects.filter(pub_id__in = pubs)
        photos_urls = PubPhotos.objects.filter(id_pub__in = pubs)

        data = {
            'title': title,
            'pubs': pubs,
            'saved_urls': saved_urls,
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
            return HttpResponse("Простите, но у Вас недостаточно прав для этой страницы. <a href='/'>На главную</a>")
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
