from django.views.generic.list import ListView
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound, Http404
# from django.views.generic.detail import DetailView

from django.shortcuts import render, redirect
from authapp.models import *
from publicationapp.models import *
from .forms import *
from django.core.files.storage import FileSystemStorage
from django.db.models.functions import Lower
# from django.db.models import Q
import operator
from django.urls import reverse


def content_images_set_fancybox_atribute(content):
    is_taking_img_url = False
    is_taking_img_tag = False
    i = 0

    while i < len(content):
        if i+4 < len(content) and content[i:(i+4)] == '<img': # если прохожясь по "content" нашлась фотография
            img_tag_start = i
            is_taking_img_tag = True
            img  = '<img'
            href = ''
            i+=4
            while is_taking_img_tag: # достать тег фотки и отдельно ссылку на неё
                img += content[i]
                if content[i:(i+5)] == 'src="':
                    img += 'rc="'
                    href = ''
                    i+=5
                    is_taking_img_url = True
                    while is_taking_img_url:
                        img  += content[i]
                        href += content[i]
                        if is_taking_img_url and content[i] == '"' and content[(i-5):i] != 'src="':
                            is_taking_img_url = False
                        i+=1
                if is_taking_img_tag and content[i] == '>':
                    is_taking_img_tag = False
                i+=1

            #   создать новый "content", в котором фотка обворачивается в ссылку для
            #   возможности её открыть и посмотреть с помошью fancybox.js
            #   (с проверкой, не было ли сделана ссылка уже ранее)
            insert = '<a data-fancybox="gallery" href="'+ href +'">' + img + '</a>'
            if (content[(img_tag_start -34 -len(href)):img_tag_start]) != ('<a data-fancybox="gallery" href="'+ href +'>'):
                content = content[:img_tag_start] + insert + content[(img_tag_start +len(img) +1):]
            i = img_tag_start + len(insert)
        i+=1
    return content


# создание новой публикации
def CreateNewPub(request):
    if not request.user.is_authenticated:
        return redirect('main')
    if not request.user.role.id in [2, 4]:
        return redirect('main')

    title = 'Создать публикацию'
    form = PubForm({'author': request.user})
    tags = Tag.objects.all()
    tag_categories = {
        'repair':   TagCategory.objects.filter(pub_type=11),
        'design':   TagCategory.objects.filter(pub_type=21),
        'lifehack': TagCategory.objects.filter(pub_type=31),
    }
    empty_tag_categories_ids = []
    selected_tags = None

    if request.method == 'POST':
        method_POST = request.POST
        form = PubForm(method_POST)

        #   проверка на корректную превьюшку
        allowed_file_formats = {
            'lifehack':          ('.mp4', '.mov', '.png', '.jpg', '.jpeg', '.gif'),
            'repair_and_design': ('.png', '.jpg', '.jpeg', '.gif'),
        }
        if 'preview' in request.FILES and request.FILES['preview']:
            if method_POST['type'] == '31' and not request.FILES['preview'].name.endswith(allowed_file_formats['lifehack']):
                form.add_error('preview', 'Пожалуйста, загрузите правильный файл! Для лайфхаков допустимы форматы файлов: ' +str(allowed_file_formats['lifehack'])[1:-1] +'.')
            if method_POST['type'] in ['11', '21'] and not request.FILES['preview'].name.endswith(allowed_file_formats['repair_and_design']):
                form.add_error('preview', 'Пожалуйста, загрузите правильное превью! Для публикаций про ремонт и дизайн допустимы форматы превью: ' +str(allowed_file_formats['repair_and_design'])[1:-1] +'.')
        else:
            message = 'Пожалуйста, загрузите превью!' if method_POST['type'] in ['11', '21'] else 'Пожалуйста, загрузите файл!'
            form.add_error('preview', message)

        #   проверка на отсутсвие введённого пользователя для авторства
        if request.user.role.id == 4 and not method_POST['author']:
            form.add_error('author', 'Пожалуйста, выберите автора для создаваемой публикаций!')

        #   проверка на уникальность заголовка
        if Publication.objects.filter(title=method_POST['title']):
            form.add_error('title', 'Публикация с таким заголовком уже существует. Пожалуйста, перефразируйте его!')

        #   проверка на пустой контент
        if method_POST['type'] != '31' and not method_POST['content'] or method_POST['content'].isspace():
            form.add_error('content', 'Пожалуйста, заполните наполнение Вашей публикации!')

        #   проверка, теги всех ли категорий
        #   выбраны и переадресация обратно, если нет
        selected_tags = Tag.objects.filter(id__in=[unit for unit in method_POST if unit.isnumeric()])
        selected_tags_categories_ids = selected_tags.values_list('category', flat=True).distinct()
        all_tag_categories_for_this_pub_type = TagCategory.objects.filter(pub_type=method_POST['type'])
        for category in all_tag_categories_for_this_pub_type:
            if category.id not in selected_tags_categories_ids:
                empty_tag_categories_ids.append(category.id)

        # если не все категории тегов выбраны или с предыдущими проверками что-т не то -- а ну-ка иди дозаполни
        if empty_tag_categories_ids or not 'preview' in request.FILES or not form.is_valid():
            content = {
            'title': title,
            'form': form,
            'pub_type': int(method_POST['type']),
            'tags': tags,
            'tag_categories': tag_categories,
            'empty_tag_categories_ids': empty_tag_categories_ids,
            'selected_tags': selected_tags,
            'action': 'create',
    		}
            return render(request, 'publicationapp/create_new_or_update.html', content)

        #   создание публикации
        pub_author = User.objects.get(id=method_POST['author']) if request.user.role.id == 4 else request.user
        cost_min = float(method_POST['cost_min'])
        cost_max = float(method_POST['cost_max'])
        if cost_min > cost_max:
            cost_min, cost_max = cost_max, cost_min
        pub_created = Publication.objects.create(
            title = method_POST['title'].capitalize(),
            type = PubTypes.objects.get(id=method_POST['type']),
            preview = ('pub_media/' + str(request.FILES['preview'])),
            author = pub_author,
            cost_min = cost_min,
            cost_max = cost_max
            )

        if pub_created.type.id != 31:
            pub_created.content = content_images_set_fancybox_atribute(method_POST['content'])
            pub_created.save()

        #   сохранение превью
        fs = FileSystemStorage()
        preview_file = fs.save(('pub_media/' + request.FILES['preview'].name), request.FILES['preview'])

        pub_created.tags.add(*selected_tags)
        pub_created.save()

        if request.user == pub_created.author:
            action_type = 5010200
            Notifications.objects.create(
                type = ActionTypes.objects.get(id=action_type),
                preview = pub_created.get_preview,
                content = 'Успешно создана публикация «' + pub_created.title +'»!',
                hover_text = 'Теперь Вы и другие пользователи могут посмотреть и воспользоваться публикацией.',
                url = reverse('pub:one', args=(pub_created.id,)),
                url_text = 'Посмотреть'
            ).receiver.add(request.user)

            JournalActions.objects.create(
                type = ActionTypes.objects.get(id=action_type),
                action_person = request.user,
                action_content = 'Создана публикация «'+ pub_created.title +'» пользователем «'+ request.user.username +'».',
                action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')], [pub_created «'+ pub_created.title +'» (id: '+ str(pub_created.id) +')]'
            )
        else:
            action_type = 9911200
            Notifications.objects.create(
                type = ActionTypes.objects.get(id=action_type),
                preview = pub_created.get_preview,
                content = 'Успешно создана публикация «' + pub_created.title +'», автором которой был назначен пользователь «'+ pub_created.author.username +'»!',
                hover_text = 'Теперь Вы и другие пользователи могут посмотреть и воспользоваться публикацией.',
                url = reverse('pub:one', args=(pub_created.id,)),
                url_text = 'Посмотреть'
            ).receiver.add(request.user)

            Notifications.objects.create(
                type = ActionTypes.objects.get(id=action_type),
                preview = pub_created.get_preview,
                content = 'Администрацией «Ремонта и Дизайна» была создана публикация «' + pub_created.title +'», автором которой были назначены Вы!',
                hover_text = 'Теперь Вы и другие пользователи могут посмотреть и воспользоваться публикацией.',
                url = reverse('pub:one', args=(pub_created.id,)),
                url_text = 'Посмотреть'
            ).receiver.add(pub_created.author)

        if User.objects.filter(following_for__id=pub_created.author.id):
            Notifications.objects.create(
                type = ActionTypes.objects.get(id=action_type),
                preview = pub_created.get_preview,
                content = 'Пользователь «'+ pub_created.author.username +'» выпустил публикацию «' + pub_created.title +'»!',
                hover_text = 'Скорее открывайте её!',
                url = reverse('pub:one', args=(pub_created.id,)),
                url_text = 'Посмотреть'
            ).receiver.add(User.objects.filter(following_for__id=pub_created.author.id))

        JournalActions.objects.create(
            type = ActionTypes.objects.get(id=action_type),
            action_person = request.user,
            action_content = 'Создана публикация «'+ pub_created.title +'» администратором «'+ request.user.username +'», который назначил пользователя в качестве «'+ pub_created.author.username +'» автора.',
            action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')], [pub_created_author «'+ pub_created.title +'» (id: '+ str(pub_created.id) +')], [pub_created «'+ pub_created.author.username +'» (id: '+ str(pub_created.author.id) +')]'
        )

        return redirect('pub:one', pk=pub_created.id)

    content = {
        'title': title,
        'form': form,
        'tags': tags,
        'tag_categories': tag_categories,
        'empty_tag_categories_ids': empty_tag_categories_ids,
        'selected_tags': selected_tags,
        'action': 'create',
		}
    return render(request, 'publicationapp/create_new_or_update.html', content)


#   редактирование публикации
def UpdatePub(request, pk):
    if not request.user.is_authenticated:
        return redirect('main')
    if not (request.user.role.id == 4 or request.user == Publication.objects.get(id=pk).author):
        return redirect('main')

    pub = Publication.objects.get(id=pk)
    author_username = 'пользователя «' + pub.author.username +'»' if pub.author else 'удалённого пользователя'
    title = 'Отредактирвать публикацию «' + pub.title +'» от ' +author_username if request.user.role.id == 4 and pub.author != request.user else 'Отредактирвать публикацию «' + pub.title +'»'
    form = PubForm({
        'title': pub.title,
        'type': pub.type,
        'author': pub.author,
        'preview': pub.preview,
        'content': pub.content,
        'cost_min': pub.cost_min,
        'cost_max': pub.cost_max,
        })
    pub_preview = pub.preview
    pub_type = pub.type.id
    tags = Tag.objects.filter(pub_type=pub.type) if request.user.role.id != 4 else Tag.objects.all()
    tag_categories = {
        'repair':   TagCategory.objects.filter(pub_type=11) if pub.type.id == 11 or request.user.role.id == 4 else None,
        'design':   TagCategory.objects.filter(pub_type=21) if pub.type.id == 21 or request.user.role.id == 4 else None,
        'lifehack': TagCategory.objects.filter(pub_type=31) if pub.type.id == 31 or request.user.role.id == 4 else None,
    }
    empty_tag_categories_ids = []
    selected_tags = pub.tags.all()

    if request.method == 'POST':
        form = PubForm(request.POST)
        method_POST = request.POST

        #   сменить тип публикации, если суперпользователь её сменил
        if request.user.role.id == 4 and 'type' in method_POST and method_POST['type']:
            pub.type = PubTypes.objects.get(id=method_POST['type'])

        #   проверка на корректную превьюшку
        allowed_file_formats = {
            'lifehack':          ('.png', '.jpg', '.jpeg', '.gif', '.mp4', '.mov'),
            'repair_and_design': ('.png', '.jpg', '.jpeg', '.gif'),
        }
        preview_name = request.FILES['preview'].name if 'preview' in request.FILES and request.FILES['preview'] else pub.preview.name
        if pub.type.id == 31 and not preview_name.endswith(allowed_file_formats['lifehack']):
            form.add_error('preview', 'Пожалуйста, загрузите правильный файл! Для лайфхаков допустимы форматы файлов: ' +str(allowed_file_formats['lifehack'])[1:-1] +'.')
        if pub.type.id in [11, 21] and not preview_name.endswith(allowed_file_formats['repair_and_design']):
            form.add_error('preview', 'Пожалуйста, загрузите правильное превью! Для публикаций про ремонт и дизайн допустимы форматы превью: ' +str(allowed_file_formats['repair_and_design'])[1:-1] +'.')

        #   проверка на отсутсвие введённого пользователя для авторства от суперпользователя
        if request.user.role.id == 4:
            if not method_POST['author']:
                form.add_error('author', 'Пожалуйста, выберите автора для редактируемой публикаций!')
            else:
                old_author = pub.author
                pub.author = User.objects.get(id=method_POST['author'])

        #   проверка на уникальность заголовка
        if Publication.objects.filter(title=method_POST['title']).exclude(id=pub.id):
            form.add_error('title', 'Публикация с таким заголовком уже существует. Пожалуйста, перефразируйте его!')

        #   проверка на пустой контент
        if method_POST['type'] != '31' and not method_POST['content'] or method_POST['content'].isspace():
            form.add_error('content', 'Пожалуйста, заполните содержание Вашей публикации!')

        #   проверка, теги всех ли категорий
        #   выбраны и переадресация обратно, если нет
        selected_tags = Tag.objects.filter(id__in=[unit for unit in method_POST if unit.isnumeric()])
        selected_tags_categories_ids = selected_tags.values_list('category', flat=True).distinct()
        all_tag_categories_for_this_pub_type = TagCategory.objects.filter(pub_type=pub.type)
        for category in all_tag_categories_for_this_pub_type:
            if category.id not in selected_tags_categories_ids:
                empty_tag_categories_ids.append(category.id)
        # если не все категории тегов выбраны или в предыдущих проверках что-то не то -- а ну-ка иди дозаполни
        if empty_tag_categories_ids or not form.is_valid():
            content = {
                'title': title,
                'form': form,
                'pub_preview': pub_preview,
                'pub_type': pub_type,
                'tags': tags,
                'tag_categories': tag_categories,
                'empty_tag_categories_ids': empty_tag_categories_ids,
                'selected_tags': selected_tags,
                'action': 'edit',
        		}
            return render(request, 'publicationapp/create_new_or_update.html', content)

        if 'preview' in request.FILES and request.FILES['preview']:
            fs = FileSystemStorage()
            preview_file = fs.save(('pub_media/' + request.FILES['preview'].name), request.FILES['preview'])
            pub.preview = 'pub_media/' + str(request.FILES['preview'])

        if pub.title != method_POST['title']:
            pub.title = method_POST['title'].capitalize()
        if pub.content != method_POST['content'] and pub.type.id != 31:
            pub.content = content_images_set_fancybox_atribute(method_POST['content'])
        if set(pub.tags.all()) != set(selected_tags):
            pub.tags.clear()
            pub.tags.add(*selected_tags)
        cost_min = float(method_POST['cost_min'])
        cost_max = float(method_POST['cost_max'])
        if cost_min > cost_max:
            cost_min, cost_max = cost_max, cost_min
        if pub.cost_min != cost_min:
            pub.cost_min = cost_min
        if pub.cost_max != cost_max:
            pub.cost_max = cost_max
        pub.save()

        if request.user == pub.author:
            Notifications.objects.create(
                type = ActionTypes.objects.get(id=5010201),
                content = 'Изменена публикация «' + pub.title +'»!',
                hover_text = 'Теперь Вы и другие пользователи могут посмотреть и воспользоваться публикацией.',
                url = reverse('pub:one', args=(pub.id,)),
                url_text = 'Посмотреть'
            ).receiver.add(request.user)

            JournalActions.objects.create(
                type = ActionTypes.objects.get(id=5010201),
                action_person = request.user,
                action_content = 'Изменена публикация «'+ pub.title +'» пользователем «'+ request.user.username +'» (её автор).',
                action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')], [pub «'+ pub.title +'» (id: '+ str(pub.id) +')]'
            )
        else:
            if old_author == pub.author:
                Notifications.objects.create(
                    type = ActionTypes.objects.get(id=9911201),
                    preview = pub.get_preview,
                    content = 'Вы изменили публикацию «' + pub.title +'»! Автор «' +pub.author.username+ '» получит уведомление об этом',
                    hover_text = 'Теперь Вы и другие пользователи могут посмотреть и воспользоваться изменённой публикацией.',
                    url = reverse('pub:one', args=(pub.id,)),
                    url_text = 'Посмотреть'
                ).receiver.add(request.user)

                Notifications.objects.create(
                    type = ActionTypes.objects.get(id=9911201),
                    preview = pub.get_preview,
                    content = 'Изменили Вашу публикацию «' + pub.title +'»! Суперпользователь: «' +request.user.username +'».',
                    hover_text = 'Теперь Вы и другие пользователи могут посмотреть и воспользоваться изменённой публикацией.',
                    url = reverse('pub:one', args=(pub.id,)),
                    url_text = 'Посмотреть'
                ).receiver.add(pub.author)

                JournalActions.objects.create(
                    type = ActionTypes.objects.get(id=5010201),
                    action_person = request.user,
                    action_content = 'Изменена публикация «'+ pub.title +'» администратором «'+ request.user.username +'» (её автор: «' +pub.author.username+ '»).',
                    action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')], [pub «'+ pub.title +'» (id: '+ str(pub.id) +')]'
                )
            else:
                if old_author:
                    Notifications.objects.create(
                        type = ActionTypes.objects.get(id=9911201),
                        preview = pub.get_preview,
                        content = 'Вы изменили публикацию «' + pub.title +'»! Новый автор «' +pub.author.username+ '» и бывший автор «' +old_author.username+ '» получат уведомление об этом.',
                        hover_text = 'Теперь Вы и другие пользователи могут посмотреть и воспользоваться изменённой публикацией.',
                        url = reverse('pub:one', args=(pub.id,)),
                        url_text = 'Посмотреть'
                    ).receiver.add(request.user)

                    Notifications.objects.create(
                        type = ActionTypes.objects.get(id=9911201),
                        preview = pub.get_preview,
                        content = 'Изменили Вашу публикацию «' + pub.title +'»! Суперпользователь: «' +request.user.username +'». По его велению теперь автор этой публикации не Вы, а «' +pub.author.username+ '».',
                        hover_text = 'Теперь Вы и другие пользователи могут посмотреть и воспользоваться изменённой публикацией.',
                        url = reverse('pub:one', args=(pub.id,)),
                        url_text = 'Посмотреть'
                    ).receiver.add(old_author)

                    Notifications.objects.create(
                        type = ActionTypes.objects.get(id=9911201),
                        preview = pub.get_preview,
                        content = 'Публикацию «' + pub.title +'» изменил суперпользователь: «' +request.user.username +'» и назначил Вас на роль автора этой публикации заместо предыдущего пользователя «' +old_author.username+ '».',
                        hover_text = 'Теперь Вы и другие пользователи могут посмотреть и воспользоваться изменённой публикацией.',
                        url = reverse('pub:one', args=(pub.id,)),
                        url_text = 'Посмотреть'
                    ).receiver.add(pub.author)

                    JournalActions.objects.create(
                        type = ActionTypes.objects.get(id=9911201),
                        action_person = request.user,
                        action_content = 'Изменена публикация «'+ pub.title +'» администратором «'+ request.user.username +'» (её старый автор: «' +old_author.username+ '», новый: «' +pub.author.username+ '»).',
                        action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')], [pub «'+ pub.title +'» (id: '+ str(pub.id) +')], [pub_old_author «'+ old_author.username +'» (id: '+ str(old_author.id) +')], [pub_new_author «'+ pub.author.username +'» (id: '+ str(pub.author.id) +')]'
                    )
                else:
                    Notifications.objects.create(
                        type = ActionTypes.objects.get(id=9911201),
                        preview = pub.get_preview,
                        content = 'Вы изменили публикацию «' + pub.title +'»! Новый автор «' +pub.author.username+ '» получит уведомление об этом, бывший автор – нет, так как он удалён.',
                        hover_text = 'Теперь Вы и другие пользователи могут посмотреть и воспользоваться изменённой публикацией.',
                        url = reverse('pub:one', args=(pub.id,)),
                        url_text = 'Посмотреть'
                    ).receiver.add(request.user)

                    Notifications.objects.create(
                        type = ActionTypes.objects.get(id=9911201),
                        preview = pub.get_preview,
                        content = 'Публикацию «' + pub.title +'» изменил суперпользователь: «' +request.user.username +'» и назначил Вас на роль автора этой публикации заместо предыдущего пользователя, который кстати по какой-то причине был удалён.',
                        hover_text = 'Теперь Вы и другие пользователи могут посмотреть и воспользоваться изменённой публикацией.',
                        url = reverse('pub:one', args=(pub.id,)),
                        url_text = 'Посмотреть'
                    ).receiver.add(pub.author)

                    if request.user.is_authenticated:
                        JournalActions.objects.create(
                            type = ActionTypes.objects.get(id=9911201),
                            action_person = request.user,
                            action_content = 'Изменена публикация «'+ pub.title +'» администратором «'+ request.user.username +'» (её старый автор: удалённый пользователь, новый: «' +pub.author.username+ '»).',
                            action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')], [pub «'+ pub.title +'» (id: '+ str(pub.id) +')], [pub_old_author DELETED], [pub_new_author «'+ pub.author.username +'» (id: '+ str(pub.author.id) +')]'
                        )

        return redirect('pub:one', pk=pub.id)

    content = {
        'title': title,
        'form': form,
        'pub_preview': pub_preview,
        'pub_type': pub_type,
        'tags': tags,
        'tag_categories': tag_categories,
        'empty_tag_categories_ids': empty_tag_categories_ids,
        'selected_tags': selected_tags,
        'action': 'edit',
		}
    return render(request, 'publicationapp/create_new_or_update.html', content)


#   удаление публикации
def DeletePub(request, pk):
    if request.user.is_authenticated and (request.user.role.id == 4 or request.user == Publication.objects.get(id=pk).author):
        pub = Publication.objects.get(id=pk)
        type = pub.type.id
        author = pub.author
        pub.delete()

        if request.user.role.id == 2 or request.user == author:
            Notifications.objects.create(
                type = ActionTypes.objects.get(id=5010500),
                preview = pub.get_preview,
                content = 'Успешно удалена публикация «' + pub.title +'» !',
                hover_text = 'Можно создать новую, ещё лучше!',
                url = reverse('pub:create_new'),
                url_text = 'Создать новую'
            ).receiver.add(author)

            JournalActions.objects.create(
                type = ActionTypes.objects.get(id=5010500),
                action_person = request.user,
                action_content = 'Удалена публикация «'+ pub.title +'» её автором «'+ author.username +'».',
                action_subjects_list = '[user «'+ author.username +'». (id: '+ str(author.id) +')], [pub_deleted «'+ pub.title +'» (id: '+ str(pub.id) +')]'
            )

        if request.user.role.id == 4 and request.user != author:
            if author:
                Notifications.objects.create(
                    type = ActionTypes.objects.get(id=9911500),
                    preview = pub.get_preview,
                    content = 'Суперпользователем была удалена Ваша публикация «' + pub.title +'» !',
                    hover_text = 'Можно создать новую, ещё лучше!',
                    url = reverse('pub:create_new'),
                    url_text = 'Создать новую'
                ).receiver.add(author)

                Notifications.objects.create(
                    type = ActionTypes.objects.get(id=9911500),
                    preview = pub.get_preview,
                    content = 'Вами была удалена публикация «' + pub.title +'» ! Жалко её автора, пользователя ' + author.username,
                    hover_text = 'Можно создать новую, ещё лучше!',
                    url = reverse('pub:create_new'),
                    url_text = 'Создать новую'
                ).receiver.add(request.user)

                JournalActions.objects.create(
                    type = ActionTypes.objects.get(id=9911500),
                    action_person = request.user,
                    action_content = 'Удалена публикация «'+ pub.title +'» администратором «'+ request.user.username +'» (её автор: «'+ pub.author.username +'»).',
                    action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')], [pub_deleted «'+ pub.title +'» (id: '+ str(pub.id) +')]'
                )
            else:
                Notifications.objects.create(
                    type = ActionTypes.objects.get(id=9911500),
                    preview = pub.get_preview,
                    content = 'Вами была удалена публикация «' + pub.title +'» ! Её автор, если что, почему-то был удалён.',
                    hover_text = 'Можно создать новую, ещё лучше!',
                    url = reverse('pub:create_new'),
                    url_text = 'Создать новую'
                ).receiver.add(request.user)

                JournalActions.objects.create(
                    type = ActionTypes.objects.get(id=9911500),
                    action_person = request.user,
                    action_content = 'Удалена публикация «'+ pub.title +'» администратором «'+ request.user.username +'» (её автор: удалённый пользователь).',
                    action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')], [pub_deleted «'+ pub.title +'» (id: '+ str(pub.id) +')]'
                )

        if type == 11:
            return redirect('repairs')
        if type == 21:
            return redirect('designs')
        if type == 31:
            return redirect('lifehacks')


#   сохранение-удаление публикаций из "Избранного"
def toggle_saved(request, pk):
    if request.is_ajax():
        if request.user.is_authenticated:
            pub = Publication.objects.get(id=pk)
            duplicate = SavedPubs.objects.filter(saver=request.user, pub=pk)

            if not duplicate:
                record = SavedPubs.objects.create(saver=request.user, pub=Publication.objects.get(id=pk))
                record.save()
                result = 1
                Notifications.objects.create(
                    type = ActionTypes.objects.get(id=5010800),
                    preview = pub.get_preview,
                    content = 'У вас новая сохранённая публикация «' + pub.title +'»!',
                    hover_text = 'Просто напоминание и благодарность за использование нашей платформой.',
                    url = reverse('saved'),
                    url_text = 'Открыть «Избранное»'
                ).receiver.add(request.user)

                if pub.author and pub.author != request.user:
                    Notifications.objects.create(
                        type = ActionTypes.objects.get(id=5010800),
                        preview = pub.get_preview,
                        content = 'Пользователь '+ request.user.username +' сохранил к себе публикацию «' + pub.title +'» !',
                        hover_text = 'Теперь у публикации ' + str( pub.saved_count ) + ' сохранений'
                    ).receiver.add(pub.author)

                JournalActions.objects.create(
                    type = ActionTypes.objects.get(id=5010800),
                    action_person = request.user,
                    action_content = 'Сохранена в «Избранное» публикация «'+ pub.title +'» пользователем «'+ request.user.username +'».',
                    action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')], [pub_saved «'+ pub.title +'» (id: '+ str(pub.id) +')]'
                )
            else:
                JournalActions.objects.create(
                    type = ActionTypes.objects.get(id=5010801),
                    action_person = request.user,
                    action_content = 'Удалена из «Избранного» публикация «'+ pub.title +'» пользователем «'+ request.user.username +'».',
                    action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')], [pub_unsaved «'+ pub.title +'» (id: '+ str(pub.id) +')]'
                )
                duplicate.delete()
                result = 0

            pub.save()

            return JsonResponse({'result': result})


#   зачисление публикаций-лайфхаков в "Просмотренные"
def set_seen(request, pk):
    if request.is_ajax():
        pub = Publication.objects.get(id=pk)

        if request.user.is_authenticated:
            user = request.user
            seen_url_object = SeenPubs.objects.get(watcher=user, pub=pub) if SeenPubs.objects.filter(watcher=user, pub=pub) else SeenPubs.objects.create(watcher=user, pub=pub)
            seen_url_object.count += 1
            seen_url_object.save()

            JournalActions.objects.create(
                type = ActionTypes.objects.get(id=4011200),
                action_person = request.user,
                action_content = 'Просмотрена публикация «'+ pub.title +'» пользователем «'+ request.user.username +'». (всего '+ str(seen_url_object.count) +')',
                action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')], [pub_seen «'+ pub.title +'» (id: '+ str(pub.id) +')]'
            )

        return JsonResponse({'result': 1})


#   смена количества "репостов" публикации при
#   нажатии пользователем на "ссылка на публикацию"
def change_shared_count(request, pk):
    if request.is_ajax():
        pub = Publication.objects.get(id=pk)
        pub.shared_count += 1
        pub.save()

        if request.user.is_authenticated:
            JournalActions.objects.create(
                type = ActionTypes.objects.get(id=5010900),
                action_person = request.user,
                action_content = 'Нажато «Поделиться» у публикации «'+ pub.title +'» пользователем «'+ request.user.username +'». (всего '+ str(pub.shared_count) +' нажатий у публикации)',
                action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')], [pub_shared «'+ pub.title +'» (id: '+ str(pub.id) +')]'
            )

        return JsonResponse({'result': str(pub)})


#   ОТФИЛЬТРОВАТЬ ПУБЛИКАЦИИ

def order_pubs_by_property(pubs, attr):
    pubs = list(pubs)
    n = 1
    while n < len(pubs):
        for i in range(len(pubs)-n):
            if getattr(pubs[i], attr) < getattr(pubs[i+1], attr):
                pubs[i], pubs[i+1] = pubs[i+1], pubs[i]
        n+=1
    return pubs

def filter_pubs (method_GET, request):
    # print(method_GET)
    pubs = Publication.objects.filter(type=method_GET['pub_type'])

    #       cost
    cost_mini = float(method_GET['cost_mini']) if 'cost_mini' in method_GET and method_GET['cost_mini'] and not method_GET['cost_mini'].isspace() else None
    cost_max  = float(method_GET['cost_max'])  if 'cost_max'  in method_GET and method_GET['cost_max']  and not method_GET['cost_max'].isspace()  else None
    cost_mini = 0 if cost_mini and cost_mini < 0 else cost_mini
    cost_max =  0 if cost_max  and cost_max  < 0 else cost_max
    if cost_mini and cost_max and cost_mini > cost_max:
        cost_mini, cost_max = cost_max, cost_mini,
    pubs = pubs.exclude(cost_max__lt=cost_mini) if cost_mini else pubs
    pubs = pubs.exclude(cost_min__gt=cost_max)  if cost_max  else pubs

    #       percent of savers by watchers
    save_percent_mini = float(method_GET['save_percent_mini']) if 'save_percent_mini' in method_GET and method_GET['save_percent_mini'] and not method_GET['save_percent_mini'].isspace() else 0
    save_percent_max  = float(method_GET['save_percent_max'])  if 'save_percent_max'  in method_GET and method_GET['save_percent_max']  and not method_GET['save_percent_max'].isspace()  else 100
    save_percent_mini = 0 if save_percent_mini < 0 else save_percent_mini
    save_percent_max =  0 if save_percent_max  < 0 else save_percent_max
    save_percent_mini = 100 if save_percent_mini > 100 else save_percent_mini
    save_percent_max =  100 if save_percent_max > 100  else save_percent_max
    if save_percent_mini and save_percent_max and save_percent_mini > save_percent_max:
        save_percent_mini, save_percent_max = save_percent_max, save_percent_mini
    ids_of_pubs_with_good_save_percent = [pub.id for pub in pubs if pub.seen_count and pub.save_percent >= save_percent_mini and pub.save_percent <= save_percent_max]
    pubs = pubs.filter(id__in=ids_of_pubs_with_good_save_percent)

    #       categories & tags
    selected_tags = Tag.objects.filter(id__in=[unit for unit in method_GET if unit.isnumeric()])
    if selected_tags:
        # проход по каждой категории и фильтрация
        # под выбранные теги именно этой категории
        for category_id in selected_tags.values_list('category', flat=True).distinct():
                pubs = pubs.filter(tags__in=selected_tags.filter(category=category_id))

    pubs = pubs.distinct()
    print('подобрано '+ str(pubs.count()) +' публикаций, тип: ' + PubTypes.objects.get(id=method_GET['pub_type']).name)

    #       ordering (сортировка по by_name возвращает list, не queryset)
    if 'ordering' in method_GET:
        pubs = pubs.order_by('-pushed')                        if method_GET['ordering'] == 'by_new'          else pubs
        pubs = pubs.order_by('pushed')                         if method_GET['ordering'] == 'by_old'          else pubs
        pubs = pubs.order_by(Lower('title'))                   if method_GET['ordering'] == 'by_name'         else pubs
        pubs = pubs.order_by('-shared_count')                  if method_GET['ordering'] == 'by_shared_count' else pubs
        pubs = order_pubs_by_property(pubs, 'seen_count')     if method_GET['ordering'] == 'by_seen_count'   else pubs
        pubs = order_pubs_by_property(pubs, 'save_percent')   if method_GET['ordering'] == 'by_savest'       else pubs
        pubs = order_pubs_by_property(pubs, 'reported_count') if method_GET['ordering'] == 'by_reports'      else pubs

    if request.user.is_authenticated:
        JournalActions.objects.create(
            type = ActionTypes.objects.get(id=5010300),
            action_person = request.user,
            action_content = 'Отфильтровал публикации пользователь «'+ request.user.username +'».',
            action_subjects_list = '[user «'+ request.user.username +'». (id: '+ str(request.user.id) +')]'
        )
    return list(pubs)


#   AJAX: узнать количество подходящих
#   публикаций под заданные фильтры
def get_filtered_pubs_count(request):
    if request.is_ajax() and request.GET:
        return JsonResponse({'pubs_count': len(filter_pubs(request.GET, request))})


#       просмотр одной публикации
class PubWatchOne(ListView):
    model = Publication
    template_name = 'publicationapp/pub_one.html'

    def get_context_data(self, **kwargs):
        context = super(PubWatchOne, self).get_context_data(**kwargs)
        saved_pubs = pub = None
        if Publication.objects.filter(id=self.kwargs['pk']):
            pub = Publication.objects.get(id=self.kwargs['pk'])
            if self.request.user.is_authenticated:
                user = self.request.user

                saved_urls = SavedPubs.objects.filter(saver=user, pub=pub)
                saved_pubs = [sp.pub.id for sp in saved_urls]

                seen_url_object = SeenPubs.objects.get(watcher=user, pub=pub) if SeenPubs.objects.filter(watcher=user, pub=pub) else SeenPubs.objects.create(watcher=user, pub=pub)
                seen_url_object.count += 1
                seen_url_object.save()

                JournalActions.objects.create(
                    type = ActionTypes.objects.get(id=4011200),
                    action_person = user,
                    action_content = 'Просмотрена публикация «'+ pub.title +'» пользователем «'+ user.username +'». (всего '+ str(seen_url_object.count) +')',
                    action_subjects_list = '[user «'+ user.username +'». (id: '+ str(user.id) +')], [pub_seen «'+ pub.title +'» (id: '+ str(pub.id) +')]'
                )
            else:
                if self.request.user.is_authenticated:
                    JournalActions.objects.create(
                        type = ActionTypes.objects.get(id=4011404),
                        action_person = self.request.user,
                        action_content = 'Попытка просмотра несуществующей публикации пользователем «'+ self.request.user.username +'».',
                        action_subjects_list = '[user «'+ self.request.user.username +'». (id: '+ str(self.request.user.id) +')], [pub_doesnt_exist_id: '+ self.kwargs['pk'] +']'
                    )

        context.update({
            'pub': pub,
            'saved_pubs': saved_pubs,
        })
        return context


# просмотр публикаций про ремонт
class RepairsWatch(ListView):
    model = Publication
    template_name = 'publicationapp/repairs.html'
    context_object_name = 'pubs'

    def get_queryset(self):
        pubs = filter_pubs(self.request.GET, self.request) if self.request.method == 'GET' and 'to_filter' in self.request.GET else list(Publication.objects.filter(type=11))
        return pubs

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(RepairsWatch, self).get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            JournalActions.objects.create(
                type = ActionTypes.objects.get(id=4021200),
                action_person = user,
                action_content = 'Просмотрены публикации про ремонт пользователем «'+ user.username +'».',
                action_subjects_list = '[user «'+ user.username +'». (id: '+ str(user.id) +')]'
            )

        tag_categories = TagCategory.objects.filter(pub_type=11)
        tags = Tag.objects.filter(category__in=tag_categories)
        selected_filters = self.request.GET if self.request.method == 'GET' and 'to_filter' in self.request.GET else {}

        context.update({
            'pubs_count': len(context['pubs']),
            'tags': tags,
            'tag_categories': tag_categories,
            'selected_filters': selected_filters,
        })
        return context


# просмотр публикаций про дизайн
class DesignsWatch(ListView):
    model = Publication
    template_name = 'publicationapp/designs.html'
    context_object_name = 'pubs'

    def get_queryset(self):
        pubs = filter_pubs(self.request.GET, self.request) if self.request.method == 'GET' and 'to_filter' in self.request.GET else list(Publication.objects.filter(type=21))
        return pubs

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(DesignsWatch, self).get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            JournalActions.objects.create(
                type = ActionTypes.objects.get(id=4022200),
                action_person = user,
                action_content = 'Просмотрены публикации про ремонт пользователем «'+ user.username +'».',
                action_subjects_list = '[user «'+ user.username +'». (id: '+ str(user.id) +')]'
            )

        saved_pubs = [sp.pub.id for sp in SavedPubs.objects.filter(saver=user, pub__type=21)] if user.is_authenticated else None
        tag_categories = TagCategory.objects.filter(pub_type=21)
        tags = Tag.objects.filter(category__in=tag_categories)
        selected_filters = self.request.GET if self.request.method == 'GET' and 'to_filter' in self.request.GET else {}

        context.update({
            'saved_pubs': saved_pubs,
            'pubs_count': len(context['pubs']),
            'tags': tags,
            'tag_categories': tag_categories,
            'selected_filters': selected_filters,
        })
        return context


# просмотр публикаций-лайфхаков
class LifehacksWatch(ListView):
    model = Publication
    template_name = 'publicationapp/lifehacks.html'
    context_object_name = 'pubs'

    def get_queryset(self):
        pubs = filter_pubs(self.request.GET, self.request) if self.request.method == 'GET' and 'to_filter' in self.request.GET else list(Publication.objects.filter(type=31))
        return pubs

    def get_context_data(self, **kwargs):
        context = super(LifehacksWatch, self).get_context_data(**kwargs)
        user = self.request.user

        if self.request.user.is_authenticated:
            JournalActions.objects.create(
                type = ActionTypes.objects.get(id=4023200),
                action_person = user,
                action_content = 'Просмотрены публикации про ремонт пользователем «'+ user.username +'».',
                action_subjects_list = '[user «'+ user.username +'». (id: '+ str(user.id) +')]'
            )

        saved_pubs = [sp.pub.id for sp in SavedPubs.objects.filter(saver=user, pub__type=31)] if user.is_authenticated else None

        tag_categories = TagCategory.objects.filter(pub_type=31)
        tags = Tag.objects.filter(category__in=tag_categories)
        selected_filters = self.request.GET if self.request.method == 'GET' and 'to_filter' in self.request.GET else {}

        context.update({
            'pubs_count': len(context['pubs']),
            'saved_pubs': saved_pubs,

            'tags': tags,
            'tag_categories': tag_categories,
            'selected_filters': selected_filters,
        })
        return context


#   просмотр публикации в "Избранном"
class Saved(ListView):
    model = SavedPubs
    template_name = 'publicationapp/saved.html'
    context_object_name = 'pubs'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return redirect('main')
        pubs = list(Publication.objects.filter(id__in=SavedPubs.objects.filter(saver=self.request.user).values_list('pub', flat=True)).order_by('-pushed'))
        return pubs

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('main')

        context = super(Saved, self).get_context_data(**kwargs)

        context.update({
            'pubs_count': len(context['pubs']),
        })
        return context
