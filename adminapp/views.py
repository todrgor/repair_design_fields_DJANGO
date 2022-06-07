from publicationapp.models import *
from authapp.models import *

from .forms import *
from django.shortcuts import render
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.utils.formats import localize
from django.urls import reverse
# from datetime import datetime
from django.core.files.storage import FileSystemStorage
from django.db.models.functions import Length

#   получение жалобы на пользователя или публикацию через ajax
@csrf_exempt
def NewComplaint(request):
    if request.user.is_authenticated:
        if request.is_ajax():
            complaint = request.POST
            contacting_support = None

            # если обращение -- жалоба на публикацию
            if int(complaint['complaint_type']) == 11:
                pub_complaint = Publication.objects.get(id=complaint['complaint_id'])
                pub_complaint.save()
                contacting_support = ContactingSupport.objects.create(title=('Жалоба на публикацию «' + pub_complaint.title +'»'), type=ContactingSupportTypes.objects.get(id=11), asked_by=request.user, ask_content=complaint['complaint_text'], ask_additional_info=complaint['complaint_id'], when_asked=timezone.now())

                Notifications.objects.create(
                    type = ActionTypes.objects.get(id=1012200),
                    preview = pub_complaint.get_preview,
                    content = 'Ваша жалоба на публикацию «'+ 'pub_complaint.title' +'» принята!',
                    hover_text = "Ждите результата здесь, в уведомлениях"
                ).receiver.add(request.user)

                if pub_complaint.author:
                    Notifications.objects.create(
                        type = ActionTypes.objects.get(id=1012200),
                        preview = pub_complaint.get_preview,
                        content = 'На Вашу публикацию «'+ pub_complaint.title +'» поступила 1 новая жалоба.',
                        hover_text = "Ждите результата здесь, в уведомлениях"
                    ).receiver.add(pub_complaint.author)

                JournalActions.objects.create(
                    type = ActionTypes.objects.get(id=1012200),
                    action_person = request.user,
                    action_content = 'Жалоба на публикацию «'+ pub_complaint.title +'» от пользователя «'+ request.user.username +'».',
                    action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')], [pub_complaint «'+ pub_complaint.title +'» (id: '+ str(pub_complaint.id) +')]',
                )

            # если обращение -- жалоба на пользователя
            if int(complaint['complaint_type']) == 12:
                user_complaint = User.objects.get(id=complaint['complaint_id'])
                user_complaint.save()
                contacting_support = ContactingSupport.objects.create(title=('Жалоба на пользователя «' + user_complaint.username +'»'), type=ContactingSupportTypes.objects.get(id=12), asked_by=request.user, ask_content=complaint['complaint_text'], ask_additional_info=complaint['complaint_id'], when_asked=timezone.now())

                Notifications.objects.create(
                    type = ActionTypes.objects.get(id=1011200),
                    preview = user_complaint.photo.name,
                    content = 'Ваша жалоба на пользователя «'+ user_complaint.username +'» принята!',
                    hover_text = "Ждите результата здесь, в уведомлениях"
                ).receiver.add(request.user)

                Notifications.objects.create(
                    type = ActionTypes.objects.get(id=1011200),
                    content = 'На Ваш профиль поступила 1 новая жалоба.',
                    hover_text = "Ждите результата здесь, в уведомлениях"
                ).receiver.add(user_complaint)

                JournalActions.objects.create(
                    type = ActionTypes.objects.get(id=1011200),
                    action_person = request.user,
                    action_content = 'Жалоба на пользователя «'+ user_complaint.username +'» от пользователя «'+ request.user.username +'».',
                    action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')], [user_complaint «'+ user_complaint.username +'» (id: '+ str(user_complaint.id) +')]',
                )

            # если обращение поступило вместе с фотками
            if request.FILES and int(complaint['complaint_type']) in [11, 12]:
                fs = FileSystemStorage()
                for one_photo in request.FILES:
                    # print(photo)
                    fs.save(('contacting_support_media/' + one_photo), request.FILES[one_photo])
                    ContactingSupportPhotos.objects.create(contacting_support_action=contacting_support, photo=('contacting_support_media/' + one_photo))

            if int(complaint['complaint_type']) in [11, 12]:
                return JsonResponse({'result': True})


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
            return resp

    def get_context_data(self, **kwargs):
        title ='Главная | Панель администратора'
        pubs = Publication.objects.filter(type__id__in=[11, 21, 31]).order_by('-pushed')[:3]
        users = User.objects.filter().order_by('-last_entry')[:4]
        tag_categories = TagCategory.objects.all().order_by('id')[:4]
        tags = [Tag.objects.annotate(text_len=Length('name')).filter(text_len__lte=20, category=category)[:4] for category in tag_categories]
        new_letters_to_support = ContactingSupport.objects.filter(answer_content=None).order_by('-when_asked')[:5]
        answered_letters_to_support = ContactingSupport.objects.exclude(answer_content=None).order_by('-when_asked')[:3] if not new_letters_to_support else None

        data = {
            'title': title,
            'pubs': pubs,
            'users': users,
            'new_letters_to_support': new_letters_to_support,
            'answered_letters_to_support': answered_letters_to_support,
    		'tags': tags,
    		'tag_categories': tag_categories,
        }
        return data


#   все обращения в поддержку:
#   их вывод и обработка администраторами
def LettersToSupport(request):
    if not request.user.is_authenticated:
        return HttpResponse("Сначала авторизируйтесь! <a href='/login/'>Авторизоваться</a>")
    if not request.user.role.id in [3, 4]:
        return HttpResponse("Простите, но у Вас недостаточно прав для этой страницы. <a href='/'>На главную</a>")

    answer_form = AnswerForm()
    answer_to_report_form = AnswerToReportForm()

    if request.method == 'POST' and ContactingSupport.objects.filter(id=int(request.POST['ask_id'])).count() >0:
        if not request.POST['answer'].isspace():
            answer = request.POST
            letter = ContactingSupport.objects.get(id=int(answer['ask_id']))
            if letter.type.id == 0 and 'delete_letter' in answer:
                Notifications.objects.create(
                    type = ActionTypes.objects.get(id=1010500),
                    content = 'Спасибо Вам за Ваше обращение! С Ваши обращением «' + letter.title + '», отправленным ' + str(localize(letter.when_asked)) + ', на каком-то этапе обработки что-то пошло не так... Оно было удалено. Если вопрос остаётся открытым, пожалуйста, сделайте обращение в поддержку ешё раз. Также: если что, на обращение был сделан ответ: «' + answer['answer'] + '». С заботой, Ваша поддержка «Ремонта и Дизайна»',
                    hover_text = "Просим прощения за неудобства ❤"
                ).receiver.add(letter.asked_by)

                JournalActions.objects.create(
                    type = ActionTypes.objects.get(id=1010500),
                    action_person = request.user,
                    action_content = 'Сломанное обращение «'+ letter.title +'» от пользователя «'+ letter.asked_by.username +'» отвечено и удалено пользователем «'+ request.user.username +'».',
                    action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')], [letter_to_support «'+ letter.title +'» (id: '+ str(letter.id) +')]',
                )

                if not letter.answer_content:
                    letter.answer_content = answer['answer']
                    letter.answered_by = request.user
                    letter.when_answered = timezone.now()
                letter.delete()

            if not letter.answer_content:
                letter_type = letter.type.id
                action_type = 1012201 if letter_type == 11 else 1011201

                if letter_type in [11, 12, 21, 22, 31, 32]:
                    letter.answer_content = answer['answer']
                    letter.answered_by = request.user
                    letter.when_answered = timezone.now()

                    if letter_type in [11, 12]:
                        letter.answer_additional_info = 0
                        pub = user = None
                        if letter_type == 11:
                            pub = Publication.objects.get(id = letter.ask_additional_info) if Publication.objects.filter(id = letter.ask_additional_info) else None
                            # noti_preview = pub.get_preview if pub else 'users_avatars/404_something_went_wrong.png'
                            report_reason_receiver = pub.author if pub else None
                        if letter_type == 12:
                            user = User.objects.get(id = letter.ask_additional_info) if User.objects.filter(id = letter.ask_additional_info) else None
                            # noti_preview = user.photo.name if user else 'users_avatars/404_something_went_wrong.png'
                            report_reason_receiver = user if user else None

                        nothing_but_just_answer = not 'is_delete_pub' in answer and not 'is_deny_rules' in answer and not 'is_delete_account' in answer
                        thats_pub_report_and_pub_author_role_id_is_4 = letter_type == 11 and pub.author.role.id == 4 if pub else None
                        thats_account_report_and_account_role_id_is_4 = letter_type == 12 and user.role.id == 4 if user else None
                        if (
                            (nothing_but_just_answer)
                         or (thats_pub_report_and_pub_author_role_id_is_4)
                         or (thats_account_report_and_account_role_id_is_4)
                            ):
                            # print('ответ только сообщением')
                            Notifications.objects.create(
                                type = ActionTypes.objects.get(id=action_type),
                                content = 'Спасибо Вам за Вашу бдительность и Вашу жалобу! ' + letter.title + ', отправленная Вами ' + str(localize(letter.when_asked)) + ', была рассмотрена.  Решение поддержки – закрыть вопрос только текстовым ответом: «' + answer['answer'] + '». Если решение не устраивает и/или не решает вопроса, подайте жалобу ещё раз, упомянув об этом. С заботой, Ваша поддержка «Ремонта и Дизайна»!',
                                hover_text = 'Если решение не устраивает, можно подать жалобу ещё раз ❤'
                            ).receiver.add(letter.asked_by)

                            if report_reason_receiver:
                                Notifications.objects.create(
                                    type = ActionTypes.objects.get(id=action_type),
                                    content = letter.title + ', отправленная пользователем «' + letter.asked_by.username + '» ' + str(localize(letter.when_asked)) + ', была рассмотрена.  Решение поддержки – закрыть вопрос только текстовым ответом: «' + answer['answer'] + '». Если решение не устраивает и/или не решает вопроса, подайте жалобу, упомянув об этом. С заботой, Ваша поддержка «Ремонта и Дизайна»!',
                                    hover_text = 'Если решение не устраивает, можно подать жалобу ❤'
                                ).receiver.add(report_reason_receiver)

                            JournalActions.objects.create(
                                type = ActionTypes.objects.get(id=action_type),
                                action_person = request.user,
                                action_content = letter.title +' от пользователя «'+ letter.asked_by.username +'» (подана '+ str(localize(letter.when_asked)) +') обработана пользователем «'+ request.user.username +'».',
                                action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')], [letter_to_support «'+ letter.title +'» (id: '+ str(letter.id) +')]',
                            )

                        else:
                            # print('ответ не только сообщением')
                            decision = ''
                            decision_for_report_reason_receiver = ''
                            if letter_type == 11 and 'is_delete_pub' in answer:
                                # print('+ удалить публикацию')
                                pub_name = '«' + pub.title + '»' if pub else '[удалена]'
                                decision = 'безвозвратно удалить публикацию ' + pub_name
                                if pub:
                                    pub.delete()
                                    letter.answer_additional_info += 10
                                else:
                                    letter.answer_additional_info += 40
                                    decision += ' (но она уже была удалена по какой-то причине)'

                            if decision:
                                decision += ' и '
                            if report_reason_receiver:
                                decision_for_report_reason_receiver = decision

                            if 'is_deny_rules' in answer and not 'is_delete_account' in answer:
                                # print('+ лишить роли')
                                report_reason_receiver_name = '«' + report_reason_receiver.username + '» ' if report_reason_receiver else '[удалён] '
                                decision += 'понизить пользователя ' + report_reason_receiver_name + 'до роли "Пользователь-зритель"'
                                if report_reason_receiver:
                                    decision_for_report_reason_receiver += 'понизить Вас до роли "Пользователь-зритель"'
                                    report_reason_receiver.role = UserRoles.objects.get(id=1)
                                    report_reason_receiver.save()
                                    letter.answer_additional_info += 100
                                else:
                                    letter.answer_additional_info += 400

                            if 'is_delete_account' in answer:
                                    # print('+ удалить аккаунт')
                                    report_reason_receiver_name = '«' + report_reason_receiver.username + '»' if report_reason_receiver else '[удалён] '
                                    decision += 'безвозвратно удалить пользователя ' + report_reason_receiver_name
                                    if report_reason_receiver:
                                        report_reason_receiver.delete()
                                        letter.answer_additional_info += 1000
                                    else:
                                        letter.answer_additional_info += 4000

                            if not report_reason_receiver:
                                decision += ' (но этот пользователь по каким-то причинам уже удалён, никаких манипуляций над ним уже не произвести)'

                            Notifications.objects.create(
                                type = ActionTypes.objects.get(id=action_type),
                                content = 'Спасибо Вам за Вашу бдительность и Вашу жалобу! ' + letter.title + ', отправленная Вами ' + str(localize(letter.when_asked)) + ', была рассмотрена.  Решение поддержки – ' + decision + '. Также ответ от поддержки: «' + answer['answer'] + '». Если решение не устраивает и/или не решает вопроса, подайте жалобу ещё раз, упомянув об этом. С заботой, Ваша поддержка «Ремонта и Дизайна»',
                                hover_text = 'Если решение не устраивает, можно подать жалобу ещё раз ❤'
                            ).receiver.add(letter.asked_by)

                            if not 'is_delete_account' in answer and report_reason_receiver:
                                Notifications.objects.create(
                                    type = ActionTypes.objects.get(id=action_type),
                                    content = letter.title + ', отправленная пользователем «' + letter.asked_by.username + '» ' + str(localize(letter.when_asked)) + ', была рассмотрена.  Решение поддержки – ' + decision_for_report_reason_receiver + '. Также ответ от поддержки: «' + answer['answer'] + '». Если решение не устраивает и/или не решает вопроса, подайте жалобу, упомянув об этом. С заботой, Ваша поддержка «Ремонта и Дизайна»',
                                    hover_text = 'Если решение не устраивает, можно подать жалобу ❤'
                                ).receiver.add(report_reason_receiver)

                            JournalActions.objects.create(
                                type = ActionTypes.objects.get(id=action_type),
                                action_person = request.user,
                                action_content = letter.title +' от пользователя «'+ letter.asked_by.username +'» (подана '+ str(localize(letter.when_asked)) +') обработана пользователем «'+ request.user.username +'».',
                                action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')], [letter_to_support «'+ letter.title +'» (id: '+ str(letter.id) +')]',
                            )

                    if letter_type in [21, 22]:
                        letter.ask_additional_info = 999
                        if letter_type == 21:
                            role_name = 'роль автора публикаций'
                            action_type = 1013201
                            role_id = 2
                        if letter_type == 22:
                            role_name = 'роль админа'
                            action_type = 1014201
                            role_id = 3

                        if letter.asked_by.role.id == 4 and User.objects.filter(role=UserRoles.objects.get(id=4)).count() <= 1:
                            Notifications.objects.create(
                                type = ActionTypes.objects.get(id=action_type),
                                content = 'Ваша заявка на '+ role_name +' была рассмотрена. На данный момент в системе всего 1 суперпользователь, поэтому нам опасно менять Вам роль. Найдите наследника и обращайтесь ещё! Также ответ от поддержки: «' + answer['answer'] +'». С заботой, Ваша поддержка «Ремонта и Дизайна»',
                                hover_text = 'По-другому пока не можем. Просим простить нас ❤'
                            ).receiver.add(letter.asked_by)

                            Notifications.objects.create(
                                type = ActionTypes.objects.get(id=action_type),
                                content = 'Заявка на '+ role_name +' от пользователя «' + letter.asked_by.username + '» никак не может быть одобрена: на данный момент в системе всего 1 суперпользователь, поэтому опасно менять ему роль. Придётся подождать наследника и обратиться потом ещё. С заботой, Ваша поддержка «Ремонта и Дизайна»',
                                hover_text = 'По-другому мы пока не можем. Вот так вот ❤'
                            ).receiver.add(request.user)

                            JournalActions.objects.create(
                                type = ActionTypes.objects.get(id=action_type),
                                action_person = request.user,
                                action_content = 'Заявка на '+ role_name +' от пользователя «'+ letter.asked_by.username +'» (подана '+ str(localize(letter.when_asked)) +') не обработана – всего 1 суперпользователь в системе.',
                                action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')], [letter_to_support «'+ letter.title +'» (id: '+ str(letter.id) +')]',
                            )

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

                            Notifications.objects.create(
                                type = ActionTypes.objects.get(id=action_type),
                                content = 'Ваша заявка на '+ role_name +' была рассмотрена. Решение: '+ decision +' Также ответ от поддержки: «' + answer['answer'] +'». С заботой, Ваша поддержка «Ремонта и Дизайна»',
                                hover_text = 'Пишите ещё, если что-то непонятно, или у Вас родилась идея! ❤'
                            ).receiver.add(letter.asked_by)

                            JournalActions.objects.create(
                                type = ActionTypes.objects.get(id=action_type),
                                action_person = request.user,
                                action_content = 'Заявка на '+ role_name +' от пользователя «'+ letter.asked_by.username +'» (подана '+ str(localize(letter.when_asked)) +') обработана пользователем «'+ request.user.username +'».',
                                action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')], [letter_to_support «'+ letter.title +'» (id: '+ str(letter.id) +')]',
                            )

                    if letter_type in [31, 32]:
                        if letter_type == 31:
                            Notifications.objects.create(
                                type = ActionTypes.objects.get(id=1010201),
                                content = 'Ваш вопрос был рассмотрен. Ответ от поддержки: «' + answer['answer'] + '».',
                                hover_text = 'Пишите ещё, если что-то непонятно, или у Вас родилась идея! ❤'
                            ).receiver.add(letter.asked_by)

                            JournalActions.objects.create(
                                type = ActionTypes.objects.get(id=1010201),
                                action_person = request.user,
                                action_content = letter.title +' от пользователя «'+ letter.asked_by.username +'» (подан '+ str(localize(letter.when_asked)) +') обработан пользователем «'+ request.user.username +'».',
                                action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')], [letter_to_support «'+ letter.title +'» (id: '+ str(letter.id) +')]',
                            )
                        if letter_type == 32:
                            Notifications.objects.create(
                                type = ActionTypes.objects.get(id=1010201),
                                content = 'Спасибо Вам за Вашу идею! Идея была рассмотрена. Ответ от поддержки: «' + answer['answer'] + '». С заботой, Ваша поддержка «Ремонта и Дизайна»',
                                hover_text = 'Ждём ещё идей! ❤'
                            ).receiver.add(letter.asked_by)

                            JournalActions.objects.create(
                                type = ActionTypes.objects.get(id=1010201),
                                action_person = request.user,
                                action_content = letter.title +' от пользователя «'+ letter.asked_by.username +'» (подана '+ str(localize(letter.when_asked)) +') обработана пользователем «'+ request.user.username +'».',
                                action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')], [letter_to_support «'+ letter.title +'» (id: '+ str(letter.id) +')]',
                            )
                letter.save()
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
    deleted_pubs_in_reports_ids = [id for id in reported_pubs_list_id if not Publication.objects.filter(id=id)]
    deleted_users_in_reports_ids = [id for id in reported_users_list_id if not User.objects.filter(id=id)]

    strange_letters = ContactingSupport.objects.filter(type=0).exclude(answer_content=None)
    new_strange_letters = ContactingSupport.objects.filter(type=0, answer_content=None)
    new_strange_letters_count = new_strange_letters.count()
    all_strange_letters_photos = ContactingSupportPhotos.objects.filter(contacting_support_action__type=0)

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
        'deleted_pubs_in_reports_ids': deleted_pubs_in_reports_ids,
        'deleted_users_in_reports_ids': deleted_users_in_reports_ids,

        'strange_letters': strange_letters,
        'new_strange_letters': new_strange_letters,
        'new_strange_letters_count': new_strange_letters_count,
        'all_strange_letters_photos': all_strange_letters_photos,

        'all_new_letters_count': ContactingSupport.objects.filter(answer_content=None).count(),
        'all_letters_count': ContactingSupport.objects.filter().count(),
        'title': title,
    }
    return render(request, 'adminapp/letters_to_support.html', content)


#   страница всех публикаций в ИС
class PubList(ListView):
    model =  Publication
    template_name = 'adminapp/publications.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated or not self.request.user.role.id in [3, 4]:
            print('проникновение туда, куда нельзя')
            return HttpResponse("Простите, но у Вас недостаточно прав для этой страницы. <a href='/'>На главную</a>")
        else:
            resp = super().get(*args, **kwargs)
            return resp

    def get_context_data(self, *, object_list=None, **kwargs):
        title ='Публикации | Панель администратора'
        pubs = Publication.objects.filter(type__id__in=[11, 21, 31])
        saved_urls = SavedPubs.objects.filter(pub__in = pubs)
        seen_urls = SeenPubs.objects.filter(pub__in = pubs)

        print(seen_urls)
        for su in seen_urls:
            print(su.pub)
            print(su.watcher)
            print(su.watcher.id)
            print(su.count)

        data = {
            'title': title,
            'pubs': pubs,
            'saved_urls': saved_urls,
            'seen_urls': seen_urls,
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
        else:
            resp = super().get(*args, **kwargs)
            return resp

    def get_context_data(self, *, object_list=None, **kwargs):
        title ='Пользователи | Панель администратора'
        users = User.objects.filter().order_by('-last_entry')
        saved_urls = SavedPubs.objects.filter()
        seen_urls = SeenPubs.objects.filter()

        data = {
            'title': title,
            'users': users,
            'saved_urls': saved_urls,
            'seen_urls': seen_urls,
        }
        return data


# страница статистики отдельного пользователя в ИС (как просили на предзащите)
def UserIndividual(request, pk):
    if not request.user.is_authenticated:
        return redirect('main')
    if request.user.role.id not in [3, 4]:
        print('проникновение туда, куда нельзя')
        return HttpResponse("Простите, но у Вас недостаточно прав для этой страницы. <a href='/'>На главную</a>")

    opened_user = User.objects.get(id=pk)
    title ='Пользователь «'+ opened_user.username +'» | Панель администратора'
    saved_urls = SavedPubs.objects.filter(saver=opened_user)
    seen_urls = SeenPubs.objects.filter(watcher=opened_user)

    JournalActions.objects.create(
        type = ActionTypes.objects.get(id=4010200),
        action_person = request.user,
        action_content = 'Просмотрена страница пользователя «'+ opened_user.username +'» пользователем «'+ request.user.username +'».',
        action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')], [opened_user «'+ opened_user.username +'». (id: '+ str(opened_user.id) +')]'
    )

    context = {
        'title': title,
        'opened_user': opened_user,
        'saved_urls': saved_urls,
        'seen_urls': seen_urls,
    }
    return render(request, 'adminapp/user_individual.html', context)


# страница журнала всех событий в ИС
class JournalList(ListView):
    model =  JournalActions
    template_name = 'adminapp/journal.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated or not self.request.user.role.id in [3, 4]:
            print('проникновение туда, куда нельзя')
            return HttpResponse("Простите, но у Вас недостаточно прав для этой страницы. <a href='/'>На главную</a>")
        else:
            resp = super().get(*args, **kwargs)
            return resp

    def get_context_data(self, *, object_list=None, **kwargs):
        title ='Журнал всех событий в ИС | Панель администратора'
        journal = JournalActions.objects.filter().order_by('-when')

        data = {
            'title': title,
            'journal': journal,
        }
        return data


#    отображение, создание,
#    редактирование и удаление тегов и их категорий
@csrf_exempt
def TagsAndTagCategories(request):
    if not request.user.is_authenticated:
        return HttpResponse("Сначала авторизируйтесь! <a href='/login/'>Авторизоваться</a>")
    if not request.user.role.id in [4]:
        HttpResponse("Простите, но у Вас недостаточно прав для этой страницы. <a href='/'>На главную</a>")

    errors = ''
    if request.method == 'POST':
        object = None
        method_POST = request.POST

        if (
                            'to_create_or_edit' in method_POST and 'tag_or_category_to_create_or_edit' in method_POST and 'category_or_tag_name' in method_POST
            and method_POST['to_create_or_edit']   and method_POST['tag_or_category_to_create_or_edit']   and method_POST['category_or_tag_name']
            ):

            if method_POST['tag_or_category_to_create_or_edit'] == 'category':
                selected_pub_types = [method_POST[item] for item in method_POST.keys() if 'pub_type_' in item]

                if method_POST['to_create_or_edit'] == 'create':
                    action_type = 2010200
                    if not TagCategory.objects.filter(name=method_POST['category_or_tag_name']) and selected_pub_types:
                        object = TagCategory.objects.create(name=method_POST['category_or_tag_name'])
                        object.pub_type.set(PubTypes.objects.filter(id__in=selected_pub_types))
                        object_type = 'создана категория «'+ object.name +'»'
                    else:
                        message = 'Для создания категории не всё заполнено!'
                        errors += message if not errors else '<br>' + message

                if method_POST['to_create_or_edit'] == 'edit':
                    action_type = 2010201
                    if 'object_id' in method_POST and method_POST['object_id'] and selected_pub_types and TagCategory.objects.filter(id=method_POST['object_id']):
                        object = TagCategory.objects.get(id=method_POST['object_id'])
                        if object.name != method_POST['category_or_tag_name']:
                            object.name = method_POST['category_or_tag_name']
                        object.pub_type.set(PubTypes.objects.filter(id__in=selected_pub_types))
                        object.save()
                        object_type = 'изменена категория «'+ object.name +'»'
                    else:
                        message = 'Для редактирования категории не всё заполнено!'
                        errors += message if not errors else '<br>' + message

            if method_POST['tag_or_category_to_create_or_edit'] == 'tag':

                if method_POST['to_create_or_edit'] == 'create':
                    action_type = 2011200
                    if 'category' in method_POST and method_POST['category'] and not Tag.objects.filter(name=method_POST['category_or_tag_name'], category=method_POST['category']):
                        object = Tag.objects.create(
                            name=method_POST['category_or_tag_name'],
                            category=TagCategory.objects.get(id=method_POST['category'])
                            )
                        object.save()
                        object_type = 'создан тег «'+ object.name +'»'
                    else:
                        message = 'Для создания тега не всё заполнено!'
                        errors += message if not errors else '<br>' + message

                if method_POST['to_create_or_edit'] == 'edit':
                    action_type = 2011201
                    if 'object_id' in method_POST and method_POST['object_id'] and 'category' in method_POST and selected_pub_types and method_POST['category'] and Tag.objects.filter(id=method_POST['object_id']):
                        object = Tag.objects.get(id=method_POST['object_id'])
                        if object.name != method_POST['category_or_tag_name'] or object.category.id != int(method_POST['category']) or set(object.pub_type.all()) != set(PubTypes.objects.filter(id__in=selected_pub_types)):
                            object.name = method_POST['category_or_tag_name']
                            object.category = TagCategory.objects.get(id=method_POST['category'])
                            object.save()
                            object_type = 'изменён тег «'+ object.name +'»'
                    else:
                        message = 'Для редактирования тега не всё заполнено!'
                        errors += message if not errors else '<br>' + message

            if object:
                Notifications.objects.create(
                    type = ActionTypes.objects.get(id=action_type),
                    content = 'Успешно '+ object_type +'!',
                    hover_text = 'Наверное умничкааа) А других уведомить и желательно ещё причину и возможности указать? А?',
                    url = reverse('admin_mine:tags_and_tag_categories'),
                    url_text = 'Теги и их категории'
                ).receiver.add(request.user)

                JournalActions.objects.create(
                    type = ActionTypes.objects.get(id=action_type),
                    action_person = request.user,
                    action_content = object_type.capitalize() +' пользователем «'+ request.user.username +'».',
                    action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')], [tag_or_tag_category «'+ str(object) +'» (id: '+ str(object.id) +')]',
                )

        if 'tag_or_category_to_delete' in method_POST and 'object_id' in method_POST and method_POST['tag_or_category_to_delete'] and method_POST['object_id']:
            if method_POST['tag_or_category_to_delete'] == 'category':
                action_type = 2010999
                object = TagCategory.objects.filter(id=method_POST['object_id'])
                if object:
                    object = TagCategory.objects.get(id=method_POST['object_id'])
                    object_type = 'удалена категория «'+ object.name +'»'

            if method_POST['tag_or_category_to_delete'] == 'tag':
                action_type = 2011999
                object = Tag.objects.filter(id=method_POST['object_id'])
                if object:
                    object = Tag.objects.get(id=method_POST['object_id'])
                    object_type = 'удалён тег «'+ object.name +'»'

            if object:
                Notifications.objects.create(
                    type = ActionTypes.objects.get(id=action_type),
                    content = 'Успешно '+ object_type +'!',
                    hover_text = 'Ну и зачем? А других уведомить и желательно ещё причину указать? А?',
                    url = reverse('admin_mine:tags_and_tag_categories'),
                    url_text = 'Теги и их категории'
                ).receiver.add(request.user)

                JournalActions.objects.create(
                    type = ActionTypes.objects.get(id=action_type),
                    action_person = request.user,
                    action_content = object_type.capitalize() +' пользователем «'+ request.user.username +'».',
                    action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')], [tag_or_tag_category «'+ str(object) +'» (id: '+ str(object.id) +')]',
                )

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
        'errors': errors,
    }
    return render(request, 'adminapp/tags_and_tag_categories.html', content)
