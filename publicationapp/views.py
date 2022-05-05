from django.views.generic.list import ListView
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, Http404
# from django.views.generic.detail import DetailView

from django.shortcuts import render, redirect
from authapp.models import *
from publicationapp.models import *
from .forms import *
from django.core.files.storage import FileSystemStorage
from django.db.models.functions import Lower
from django.db.models import Sum
# from django.db.models import Q
import operator



# def is_number(s):
#     try:
#         float(s)
#         return True
#     except ValueError:
#         return False


# создание новой публикации
def CreateNewPub(request):
    if request.user.is_authenticated:
        if request.user.role.id in [2, 4]:
            title = 'Создать публикацию'
            form = PubForm()
            tags = Tag.objects.all()
            tag_categories = {
                'repair':   TagCategory.objects.filter(id__in=tags.filter(pub_type=11).values_list('category', flat=True)),
                'design':   TagCategory.objects.filter(id__in=tags.filter(pub_type=21).values_list('category', flat=True)),
                'lifehack': TagCategory.objects.filter(id__in=tags.filter(pub_type=31).values_list('category', flat=True)),
            }
            empty_tag_categories_ids = []
            selected_tags = None

            # if request.method == 'POST':
            #     print(request.POST)

            if request.method == 'POST':
                method_POST = request.POST
                form = PubForm(method_POST)

                #   проверка, теги всех ли категорий
                #   выбраны и переадресация обратно, если нет
                selected_tags = Tag.objects.filter(id__in=[unit for unit in method_POST if unit.isnumeric()], pub_type=method_POST['type'])
                selected_tags_categories_ids = selected_tags.values_list('category', flat=True).distinct()
                all_tag_categories_for_this_pub_type = TagCategory.objects.filter(id__in=Tag.objects.filter(pub_type=method_POST['type']).values_list('category', flat=True))
                for category in all_tag_categories_for_this_pub_type:
                    if category.id not in selected_tags_categories_ids:
                        empty_tag_categories_ids.append(category.id)
                if empty_tag_categories_ids:
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

                #   создание публикции
                pub_created = Publication.objects.create(title=method_POST['title'].capitalize(), type=PubTypes.objects.get(id=method_POST['type']), preview=('pub_media/' + str(request.FILES['preview'])), content_first_desc=method_POST['content_first_desc'], content_last_desc=method_POST['content_last_desc'], author=User.objects.get(id=request.user.id))

                #   сохранение превью и фотографий внутри публикции
                fs = FileSystemStorage()
                preview_file = fs.save(('pub_media/' + request.FILES['preview'].name), request.FILES['preview'])
                if method_POST['type'] in ['11', '12'] and 'photo' in request.FILES:
                    photos = request.FILES.getlist('photo')
                    i_count = 0
                    for i in photos:
                        fs.save(('pub_media/' + photos[i_count].name), photos[i_count])
                        PubPhotos.objects.create(id_pub=Publication.objects.get(id=pub_created.id), photo=('pub_media/' + photos[i_count].name))
                        i_count +=1

                pub_created.tags.add(*selected_tags)
                pub_created.cost_min = method_POST['cost_min']
                pub_created.cost_max = method_POST['cost_max']
                pub_created.save()

                noti=Publication.objects.create(title=('Успешно создана публикация «' + pub_created.title +'» !'), type=PubTypes.objects.get(id=51), preview=(pub_created.preview.name), content_first_desc="Теперь Вы и другие пользвователи могут посмотреть и воспользоваться публикацией.", content_last_desc='', author=request.user)
                Notifications.objects.create(user_receiver=request.user, noti_for_user=noti)
                noti=Publication.objects.create(title=('Пользователь '+ pub_created.author.username +' выпустил публикацию «' + pub_created.title +'» !'), type=PubTypes.objects.get(id=51), preview=(pub_created.preview.name), content_first_desc="Скорее открывайте её!", content_last_desc='', author=request.user)
                for s in UserSubscribes.objects.filter(star_id=pub_created.author.id):
                    Notifications.objects.create(user_receiver=s.subscriber_id, noti_for_user=noti)
                return redirect('pub:pub_one', pk=pub_created.id)
                # except:
                #     form.add_error(None, 'Ошибка создания публикции')

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
        else:
            return redirect('main')
    else:
        return redirect('main')


# удаление публикации
def DeletePub(request, pk):
    if request.user.is_authenticated and request.user.role.id in [2, 4]:
        pub = Publication.objects.get(id=pk)
        type = pub.type.id
        author = pub.author
        pub.delete()

        if request.user.role.id == 2:
            noti=Publication.objects.create(title=('Успешно удалена публикация «' + pub.title +'» !'), type=PubTypes.objects.get(id=51), preview=(pub.preview.name), content_first_desc="Можно создать новую, ещй лучше!", content_last_desc='', author=request.user)
            Notifications.objects.create(user_receiver=request.user, noti_for_user=noti)
        if request.user.role.id == 4:
            noti=Publication.objects.create(title=('Суперпользователем была удалена Ваша публикация «' + pub.title +'» !'), type=PubTypes.objects.get(id=51), preview=(pub.preview.name), content_first_desc="Можно создать новую, ещй лучше!", content_last_desc='', author=request.user)
            Notifications.objects.create(user_receiver=author, noti_for_user=noti)
            noti=Publication.objects.create(title=('Вами была удалена публикация «' + pub.title +'» ! Жалко его автора, пользователя ' + author.username), type=PubTypes.objects.get(id=51), preview=(pub.preview.name), content_first_desc="Можно создать новую, ещй лучше!", content_last_desc='', author=request.user)
            Notifications.objects.create(user_receiver=request.user, noti_for_user=noti)

        if type == 11:
            return redirect('pub:repairs')
        if type == 21:
            return redirect('pub:designs')
        if type == 31:
            return redirect('pub:lifehacks')


#   редактирование публикации
def UpdatePub(request, pk):
    if request.user.is_authenticated:
        if request.user.role.id in [2, 4]:
            pub = Publication.objects.get(id=pk)
            photos = PubPhotos.objects.filter(id_pub=pk)
            title = 'Отредактирвать публикацию пользователя ' + pub.author.username if request.user.role.id == 4 and pub.author != request.user else 'Отредактирвать публикацию'
            form = PubForm()
            tags = Tag.objects.filter(pub_type=pub.type)
            tag_categories = {
                'repair':   TagCategory.objects.filter(id__in=tags.filter(pub_type=11).values_list('category', flat=True)) if pub.type.id == 11 else None,
                'design':   TagCategory.objects.filter(id__in=tags.filter(pub_type=21).values_list('category', flat=True)) if pub.type.id == 21 else None,
                'lifehack': TagCategory.objects.filter(id__in=tags.filter(pub_type=31).values_list('category', flat=True)) if pub.type.id == 31 else None,
            }
            empty_tag_categories_ids = []
            selected_tags = pub.tags.all()

            if request.method == 'POST':
                form = PubForm(request.POST)
                method_POST = request.POST

                #   проверка, теги всех ли категорий
                #   выбраны и переадресация обратно, если нет
                selected_tags = Tag.objects.filter(id__in=[unit for unit in method_POST if unit.isnumeric()], pub_type=pub.type)
                selected_tags_categories_ids = selected_tags.values_list('category', flat=True).distinct()
                all_tag_categories_for_this_pub_type = TagCategory.objects.filter(id__in=Tag.objects.filter(pub_type=pub.type).values_list('category', flat=True))
                for category in all_tag_categories_for_this_pub_type:
                    if category.id not in selected_tags_categories_ids:
                        empty_tag_categories_ids.append(category.id)
                if empty_tag_categories_ids:
                    content = {
                        'title': title,
                        'form': form,
                        'tags': tags,
                        'tag_categories': tag_categories,
                        'empty_tag_categories_ids': empty_tag_categories_ids,
                        'selected_tags': selected_tags,
                        'action': 'edit',
                		}
                    return render(request, 'publicationapp/create_new_or_update.html', content)

                pub.__dict__.update({'title': method_POST['title'].capitalize(), 'preview': ('pub_media/' + str(request.FILES['preview'])), 'content_first_desc': method_POST['content_first_desc'], 'content_last_desc': method_POST['content_last_desc']})
                fs = FileSystemStorage()
                preview_file = fs.save(('pub_media/' + request.FILES['preview'].name), request.FILES['preview'])
                if pub.type.id in [11, 12]:
                    if 'photo' in request.FILES:
                        photos = request.FILES.getlist('photo')
                        PubPhotos.objects.filter(id_pub=pub.id).delete()
                        i_count = 0
                        for i in photos:
                            fs.save(('pub_media/' + photos[i_count].name), photos[i_count])
                            PubPhotos.objects.create(id_pub=Publication.objects.get(id=pub.id), photo=('pub_media/' + photos[i_count].name))
                            i_count +=1

                pub.tags.clear()
                pub.tags.add(*selected_tags)
                pub.cost_min = method_POST['cost_min']
                pub.cost_max = method_POST['cost_max']
                pub.save()

                if request.user.role.id == 2:
                    noti=Publication.objects.create(title=('Изменена публикация «' + pub.title +'» !'), type=PubTypes.objects.get(id=51), preview=(pub.preview.name), content_first_desc="Теперь Вы и другие пользвователи могут посмотреть и воспользоваться изменённой публикацией.", content_last_desc='', author=request.user)
                    Notifications.objects.create(user_receiver=request.user, noti_for_user=noti)
                if request.user.role.id == 4:
                    noti=Publication.objects.create(title=('Вы изменили публикацию «' + pub.title +'» ! Автор ' +pub.author.username+ ' получит уведомление об этом'), type=PubTypes.objects.get(id=51), preview=(pub.preview.name), content_first_desc="Теперь Вы и другие пользвователи могут посмотреть и воспользоваться изменённой публикацией.", content_last_desc='', author=request.user)
                    Notifications.objects.create(user_receiver=request.user, noti_for_user=noti)
                    noti=Publication.objects.create(title=('Изменили Вашу публикацию «' + pub.title +'» ! Суперпользователь: ' +request.user.username), type=PubTypes.objects.get(id=51), preview=(pub.preview.name), content_first_desc="Теперь Вы и другие пользвователи могут посмотреть и воспользоваться изменённой публикацией.", content_last_desc='', author=request.user)
                    Notifications.objects.create(user_receiver=pub.author, noti_for_user=noti)

                return redirect('pub:pub_one', pk=pub.id)

            form = PubForm({
                'title': pub.title,
                'type': pub.type,
                'preview': pub.preview,
                'content_first_desc': pub.content_first_desc,
                'content_last_desc': pub.content_last_desc,
                'cost_min': pub.cost_min,
                'cost_max': pub.cost_max,
                'photo': photos
                })

            content = {
                'title': title,
                'form': form,
                'tags': tags,
                'tag_categories': tag_categories,
                'empty_tag_categories_ids': empty_tag_categories_ids,
                'selected_tags': selected_tags,
                'action': 'edit',
        		}
            return render(request, 'publicationapp/create_new_or_update.html', content)
        else:
            return redirect('main')
    else:
        return redirect('main')


#   просмотр публикции в "Избранном"
class Saved(ListView):
    model = SavedPubs
    template_name = 'publicationapp/saved.html'
    context_object_name = 'pubs'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return redirect('main')
        return Publication.objects.filter(id__in=SavedPubs.objects.filter(saver_id=self.request.user).values_list('pub_id', flat=True)).order_by('-pushed')

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('main')

        context = super(Saved, self).get_context_data(**kwargs)
        subscribes_urls = UserSubscribes.objects.filter(subscriber_id=self.request.user)
        subscribing_authors = [sa.star_id.id for sa in subscribes_urls]

        context.update({
            'subscribing_authors': subscribing_authors,
        })
        return context


#   сохранение-удаление публикаций из "Избранного"
def toggle_saved(request, pk):
    if request.is_ajax():
        if request.user.is_authenticated:
            duplicate = SavedPubs.objects.filter(saver_id=request.user, pub_id=pk)

            if not duplicate:
                record = SavedPubs.objects.create(saver_id=request.user, pub_id=Publication.objects.get(id=pk))
                record.save()
                result = 1
            else:
                duplicate.delete()
                result = 0

            pub = Publication.objects.get(id=pk)
            pub.saved_count = SavedPubs.objects.filter(pub_id__id=pk).count()
            pub.save()
            # context = {
            #     'user': request.user,
            #     'news_item': NewsItem.objects.get(pk=pk)
            # }

            # result = render_to_string('newsapp/includes/likes_block.html', context)
            noti=Publication.objects.create(title=('У вас новая сохранённая публикация «' + pub.title +'» !'), type=PubTypes.objects.get(id=51), preview=(pub.preview.name), content_first_desc="Просто напоминание и благодарность за использование нашей ИС.", content_last_desc='', author=request.user)
            Notifications.objects.create(user_receiver=request.user, noti_for_user=noti)
            noti=Publication.objects.create(title=('Пользователь '+ request.user.username +' сохранил к себе публикацию «' + pub.title +'» !'), type=PubTypes.objects.get(id=51), preview=(request.user.photo.name), content_first_desc=("Теперь у публикации " + str( SavedPubs.objects.filter(pub_id=pub.id).count() ) + " сохранений"), content_last_desc='', author=request.user)
            Notifications.objects.create(user_receiver=pub.author, noti_for_user=noti)

            return JsonResponse({'result': result})


#   зачисление публикаций-лайфхаков в "Просмотренные"
def set_seen(request, pk):
    if request.is_ajax():
        pub = Publication.objects.get(id=pk)
        pub.seen_count +=1
        pub.save()

        if request.user.is_authenticated:
            user = request.user
            seen_url_object = SeenPubs.objects.get(watcher_id=user, pub_id=pub) if SeenPubs.objects.filter(watcher_id=user, pub_id=pub) else SeenPubs.objects.create(watcher_id=user, pub_id=pub)
            seen_url_object.count += 1
            seen_url_object.save()

        return JsonResponse({'result': 1})


#   смена количества "репостов" публикации при
#   нажатии пользователем на "ссылка на публикацию"
def change_shared_count(request, pk):
    if request.is_ajax():
        pub = Publication.objects.get(id=pk)
        pub.shared_count += 1
        pub.save()
        return JsonResponse({'result': str(pub)})


#   ОТФИЛЬТРОВАТЬ ПУБЛИКАЦИИ
def filter_pubs (method_GET):
    # print(method_GET)
    pubs = Publication.objects.filter(type=method_GET['pub_type'])

    #       cost
    cost_mini = float(method_GET['cost_mini']) if 'cost_mini' in method_GET and method_GET['cost_mini'] and not method_GET['cost_mini'].isspace() else None
    cost_max  = float(method_GET['cost_max'])  if 'cost_max'  in method_GET and method_GET['cost_max']  and not method_GET['cost_max'].isspace()  else None
    cost_mini = 0 if cost_mini and cost_mini < 0 else cost_mini
    cost_max =  0 if cost_max  and cost_max  < 0 else cost_max
    if cost_mini and cost_max and cost_mini > cost_max:
        a = cost_mini
        cost_mini = cost_max
        cost_max = a
    pubs = pubs.exclude(cost_max__lt=cost_mini) if cost_mini else pubs
    pubs = pubs.exclude(cost_min__gt=cost_max)  if cost_max  else pubs
    # method_GET['cost_mini'] = cost_mini
    # method_GET['cost_max'] = cost_max

    #       percent of savers by watchers
    save_percent_mini = float(method_GET['save_percent_mini']) if 'save_percent_mini' in method_GET and method_GET['save_percent_mini'] and not method_GET['save_percent_mini'].isspace() else 0
    save_percent_max  = float(method_GET['save_percent_max'])  if 'save_percent_max'  in method_GET and method_GET['save_percent_max']  and not method_GET['save_percent_max'].isspace()  else 100
    # print (save_percent_mini, save_percent_max)
    save_percent_mini = 0 if save_percent_mini < 0 else save_percent_mini
    save_percent_max =  0 if save_percent_max  < 0 else save_percent_max
    save_percent_mini = 100 if save_percent_mini > 100 else save_percent_mini
    save_percent_max =  100 if save_percent_max > 100  else save_percent_max
    if save_percent_mini and save_percent_max and save_percent_mini > save_percent_max:
        a = save_percent_mini
        save_percent_mini = save_percent_max
        save_percent_max = a
    ids_of_pubs_with_good_save_percent = [pub.id for pub in pubs if pub.seen_count and (pub.saved_count/pub.seen_count*100) >= save_percent_mini and (pub.saved_count/pub.seen_count*100) <= save_percent_max]
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
        pubs = pubs.order_by('-pushed')         if method_GET['ordering'] == 'by_new'          else pubs
        pubs = pubs.order_by('pushed')          if method_GET['ordering'] == 'by_old'          else pubs
        pubs = pubs.order_by('-seen_count')     if method_GET['ordering'] == 'by_seen_count'   else pubs
        pubs = pubs.order_by('-saved_count')    if method_GET['ordering'] == 'by_savest'       else pubs
        # pubs = pubs.order_by('seen_count'/'saved_count') if method_GET['ordering'] == 'by_savest' else pubs
        pubs = pubs.order_by('-shared_count')   if method_GET['ordering'] == 'by_shared_count' else pubs
        pubs = pubs.order_by('-reported_count') if method_GET['ordering'] == 'by_reports'      else pubs
        # ну почему сортировка по наименованию для русского языка не работает((((
        pubs = pubs.order_by(Lower('title'))    if method_GET['ordering'] == 'by_name' else pubs
        # pubs = sorted(pubs, key=operator.attrgetter('title')) if method_GET['ordering'] == 'by_name' else pubs

    # [pub.id for pub in sorted(pubs, key=operator.attrgetter('title'))]
    # print(pubs.order_by(Lower('title')))
    # print(sorted(pubs, key=operator.attrgetter('title')))
    # print(pubs.order_by(Lower('title').desc()))
    # print(pubs.annotate(a=Lower('title')).order_by('a'))
    return pubs


#   AJAX: узнать количество подходящих
#   публикаций под заданные фильтры
def get_filtered_pubs_count(request):
    if request.is_ajax() and request.GET:
        return JsonResponse({'pubs_count': filter_pubs(request.GET).count()})


#       просмотр одной публикации
class PubWatchOne(ListView):
    model = Publication
    template_name = 'publicationapp/pub_one.html'
    context_object_name = 'pub'
    allow_empty = False # сделать ответ на случай, если публикации с введённым id не существует

    def get_queryset(self):
        return Publication.objects.get(id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(PubWatchOne, self).get_context_data(**kwargs)
        pub = Publication.objects.get(id=self.kwargs['pk'])

        saved_pubs = subscribing_authors =  None
        if self.request.user.is_authenticated:
            user = self.request.user

            saved_urls = SavedPubs.objects.filter(saver_id=user, pub_id=pub)
            saved_pubs = [sp.pub_id.id for sp in saved_urls]
            subscribes_urls = UserSubscribes.objects.filter(subscriber_id=user)
            subscribing_authors = [sa.star_id.id for sa in subscribes_urls]

            seen_url_object = SeenPubs.objects.get(watcher_id=user, pub_id=pub) if SeenPubs.objects.filter(watcher_id=user, pub_id=pub) else SeenPubs.objects.create(watcher_id=user, pub_id=pub)
            seen_url_object.count += 1
            seen_url_object.save()

        #   обновление статистики у открываемой публикции
        ages = (SeenPubs.objects.filter(pub_id=self.kwargs['pk']).aggregate(Sum('watcher_id__age')))['watcher_id__age__sum']
        pub.average_age_watchers = ages / SeenPubs.objects.filter(pub_id=pub).count()  if SeenPubs.objects.filter(pub_id=pub).count() != 0  else 0
        pub.average_age_savers =   ages / SavedPubs.objects.filter(pub_id=pub).count() if SavedPubs.objects.filter(pub_id=pub).count() != 0 else 0
        pub.seen_count +=1
        pub.save()

        context.update({
            'pub': pub,
            'photos': PubPhotos.objects.filter(id_pub=pub),
            'saved_pubs': saved_pubs,
            'subscribing_authors': subscribing_authors,
        })
        return context


# просмотр публикаций про ремонт
class RepairsWatch(ListView):
    model = Publication
    template_name = 'publicationapp/repairs.html'
    context_object_name = 'pubs'

    def get_queryset(self):
        pubs = filter_pubs(self.request.GET) if self.request.method == 'GET' and 'to_filter' in self.request.GET else Publication.objects.filter(type=11)
        return pubs

    def get_context_data(self, **kwargs):
        context = super(RepairsWatch, self).get_context_data(**kwargs)

        tags = Tag.objects.filter(pub_type=PubTypes.objects.get(id=11))
        tag_categories = TagCategory.objects.filter(id__in=tags.values_list('category', flat=True))
        selected_filters = self.request.GET if self.request.method == 'GET' and 'to_filter' in self.request.GET else {}

        context.update({
            # 'all_tags_for_this_pubs': all_tags_for_this_pubs,
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
        pubs = filter_pubs(self.request.GET) if self.request.method == 'GET' and 'to_filter' in self.request.GET else Publication.objects.filter(type=21)
        return pubs

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(DesignsWatch, self).get_context_data(**kwargs)
        saved_pubs = [sp.pub_id.id for sp in SavedPubs.objects.filter(saver_id=user, pub_id__type=21)] if user.is_authenticated else None

        tags = Tag.objects.filter(pub_type=PubTypes.objects.get(id=21))
        tag_categories = TagCategory.objects.filter(id__in=tags.values_list('category', flat=True))
        selected_filters = self.request.GET if self.request.method == 'GET' and 'to_filter' in self.request.GET else {}

        context.update({
            # 'all_tags_for_this_pubs': all_tags_for_this_pubs,
            'saved_pubs': saved_pubs,
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

        #   обновление статистики у открываемой публикции
        for pub in Publication.objects.filter(type=31):
            ages = (SeenPubs.objects.filter(pub_id=pub).aggregate(Sum('watcher_id__age')))['watcher_id__age__sum']
            pub.average_age_watchers = ages / SeenPubs.objects.filter(pub_id=pub).count()  if SeenPubs.objects.filter(pub_id=pub).count() != 0  else 0
            pub.average_age_savers =   ages / SavedPubs.objects.filter(pub_id=pub).count() if SavedPubs.objects.filter(pub_id=pub).count() != 0 else 0
            pub.seen_count +=1
            pub.save()

        pubs = filter_pubs(self.request.GET) if self.request.method == 'GET' and 'to_filter' in self.request.GET else Publication.objects.filter(type=31)
        return pubs

    def get_context_data(self, **kwargs):
        context = super(LifehacksWatch, self).get_context_data(**kwargs)
        user = self.request.user

        saved_pubs =          [sp.pub_id.id for sp in SavedPubs.objects.filter(saver_id=user, pub_id__type=31)] if user.is_authenticated else None
        subscribing_authors = [sa.star_id.id for sa in (UserSubscribes.objects.filter(subscriber_id=user))]     if user.is_authenticated else None

        tags = Tag.objects.filter(pub_type=PubTypes.objects.get(id=31))
        tag_categories = TagCategory.objects.filter(id__in=tags.values_list('category', flat=True))
        selected_filters = self.request.GET if self.request.method == 'GET' and 'to_filter' in self.request.GET else {}

        context.update({
            'saved_pubs': saved_pubs,
            'subscribing_authors': subscribing_authors,

            'tags': tags,
            'tag_categories': tag_categories,
            'selected_filters': selected_filters,
        })
        return context
