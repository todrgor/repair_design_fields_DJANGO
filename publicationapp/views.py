from django.views.generic.list import ListView
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, Http404
# from django.views.generic.detail import DetailView

from django.shortcuts import render, redirect
from authapp.models import *
from publicationapp.models import *
from .forms import *
from django.core.files.storage import FileSystemStorage

def CreateNewPub(request):
    form = PubForm()
    if request.method == 'POST':
        form = PubForm(request.POST)
        pub_post = request.POST
        # try:
        Publication.objects.create(title=pub_post['title'], role=PubRoles.objects.get(id=pub_post['role']), preview=('pub_media/' + str(request.FILES['preview'])), content_first_desc=pub_post['content_first_desc'], content_last_desc=pub_post['content_last_desc'], author=User.objects.get(id=request.user.id))
        fs = FileSystemStorage()
        preview_file = fs.save(('pub_media/' + request.FILES['preview'].name), request.FILES['preview'])
        pub_created = Publication.objects.get(title=pub_post['title'], role=pub_post['role'], preview=('pub_media/' + str(request.FILES['preview'])), content_first_desc=pub_post['content_first_desc'], content_last_desc=pub_post['content_last_desc'], author=User.objects.get(id=request.user.id))
        if pub_post['role'] == '11' or pub_post['role'] == '21':
            if request.FILES['photo']:
                photos = request.FILES.getlist('photo')
                i_count = 0
                for i in photos:
                    fs.save(('pub_media/' + photos[i_count].name), photos[i_count])
                    PubPhotos.objects.create(id_pub=Publication.objects.get(id=pub_created.id), photo=('pub_media/' + photos[i_count].name))
                    i_count +=1

        if pub_post['role'] == '11':
            pub_created.cost_min = pub_post['cost_min']
            pub_created.cost_max = pub_post['cost_max']
            pub_created.save()
            PubHasTags.objects.create(pub_id=Publication.objects.get(id=pub_created.id), tag_id=TagName.objects.get(id=pub_post['tag_repair_what_to']))
            PubHasTags.objects.create(pub_id=Publication.objects.get(id=pub_created.id), tag_id=TagName.objects.get(id=pub_post['tag_repair_by_what']))
            PubHasTags.objects.create(pub_id=Publication.objects.get(id=pub_created.id), tag_id=TagName.objects.get(id=pub_post['tag_repair_where']))
        if pub_post['role'] == '21':
            pub_created.cost_min = pub_post['cost_min']
            pub_created.cost_max = pub_post['cost_max']
            pub_created.save()
            PubHasTags.objects.create(pub_id=Publication.objects.get(id=pub_created.id), tag_id=TagName.objects.get(id=pub_post['tag_design_room']))
            PubHasTags.objects.create(pub_id=Publication.objects.get(id=pub_created.id), tag_id=TagName.objects.get(id=pub_post['tag_design_style']))
        if pub_post['role'] == '31':
            PubHasTags.objects.create(pub_id=Publication.objects.get(id=pub_created.id), tag_id=TagName.objects.get(id=pub_post['tag_lifehack_lifesphere']))

        return redirect('pub:pub_one', pk=pub_created.id)
        # except:
        #     form.add_error(None, 'Ошибка создания публикции')

    title = 'Создать публикацию'
    return render(request, 'publicationapp/create_new_or_update.html', {'title': title, 'form': form, })

def DeletePub(request, pk):
    pub = Publication.objects.get(id=pk)
    role = pub.role.id
    pub.delete()
    if role == 11:
        return redirect('pub:repairs')
    if role == 21:
        return redirect('pub:designs')
    if role == 31:
        return redirect('pub:lifehacks')

def UpdatePub(request, pk):
    pub = Publication.objects.get(id=pk)
    photos = PubPhotos.objects.filter(id_pub=pk)
    tags = PubHasTags.objects.filter(pub_id=pk)

    tag_repair_what_to = None
    tag_repair_by_what = None
    tag_repair_where = None
    tag_design_room = None
    tag_design_style = None
    tag_lifehack_lifesphere = None

    if request.method == 'POST':
        form = PubForm(request.POST)
        pub_post = request.POST
        pub.__dict__.update({'title': pub_post['title'], 'role': PubRoles.objects.get(id=pub_post['role']), 'preview': ('pub_media/' + str(request.FILES['preview'])), 'content_first_desc': pub_post['content_first_desc'], 'content_last_desc': pub_post['content_last_desc'], 'author': User.objects.get(id=request.user.id)})
        fs = FileSystemStorage()
        preview_file = fs.save(('pub_media/' + request.FILES['preview'].name), request.FILES['preview'])
        if pub_post['role'] == '11' or pub_post['role'] == '21':
            if request.FILES['photo']:
                photos = request.FILES.getlist('photo')
                PubPhotos.objects.filter(id_pub=pub.id).delete()
                i_count = 0
                for i in photos:
                    fs.save(('pub_media/' + photos[i_count].name), photos[i_count])
                    PubPhotos.objects.create(id_pub=Publication.objects.get(id=pub.id), photo=('pub_media/' + photos[i_count].name))
                    i_count +=1
        PubHasTags.objects.filter(pub_id=pub.id).delete()
        if pub_post['role'] == '11':
            pub.cost_min = pub_post['cost_min']
            pub.cost_max = pub_post['cost_max']
            PubHasTags.objects.create(pub_id=Publication.objects.get(id=pub.id), tag_id=TagName.objects.get(id=pub_post['tag_repair_what_to']))
            PubHasTags.objects.create(pub_id=Publication.objects.get(id=pub.id), tag_id=TagName.objects.get(id=pub_post['tag_repair_by_what']))
            PubHasTags.objects.create(pub_id=Publication.objects.get(id=pub.id), tag_id=TagName.objects.get(id=pub_post['tag_repair_where']))
        if pub_post['role'] == '21':
            pub.cost_min = pub_post['cost_min']
            pub.cost_max = pub_post['cost_max']
            PubHasTags.objects.create(pub_id=Publication.objects.get(id=pub.id), tag_id=TagName.objects.get(id=pub_post['tag_design_room']))
            PubHasTags.objects.create(pub_id=Publication.objects.get(id=pub.id), tag_id=TagName.objects.get(id=pub_post['tag_design_style']))
        if pub_post['role'] == '31':
            PubHasTags.objects.create(pub_id=Publication.objects.get(id=pub.id), tag_id=TagName.objects.get(id=pub_post['tag_lifehack_lifesphere']))
        pub.save()
        return redirect('pub:pub_one', pk=pub.id)

    if pub.role.id == 11:
        for t in tags:
            if t.tag_id.tag_category == 'Ремонт чего':
                tag_repair_what_to = t.tag_id.id
            if t.tag_id.tag_category == 'Инструмент':
                tag_repair_by_what = t.tag_id.id
            if t.tag_id.tag_category == 'В помещении':
                tag_repair_where = t.tag_id.id
        form = PubForm({'title': pub.title, 'role': pub.role, 'preview': pub.preview, 'content_first_desc': pub.content_first_desc, 'content_last_desc': pub.content_last_desc, 'cost_min': pub.cost_min, 'cost_max': pub.cost_max, 'photo': photos, 'tag_repair_what_to': tag_repair_what_to, 'tag_repair_by_what': tag_repair_by_what, 'tag_repair_where': tag_repair_where, })

    if pub.role.id == 21:
        for t in tags:
            if t.tag_id.tag_category == 'Комната':
                tag_design_room = t.tag_id.id
            if t.tag_id.tag_category == 'Основной стиль':
                tag_design_style = t.tag_id.id
        form = PubForm({'title': pub.title, 'role': pub.role, 'preview': pub.preview, 'content_first_desc': pub.content_first_desc, 'content_last_desc': pub.content_last_desc, 'cost_min': pub.cost_min, 'cost_max': pub.cost_max, 'photo': photos, 'tag_design_room': tag_design_room, 'tag_design_style': tag_design_style, })

    if pub.role.id == 31:
        for t in tags:
            if t.tag_id.tag_category == 'В сфере жизни':
                tag_lifehack_lifesphere = t.tag_id.id
        form = PubForm({'title': pub.title, 'role': pub.role, 'preview': pub.preview, 'content_first_desc': pub.content_first_desc, 'content_last_desc': pub.content_last_desc, 'cost_min': pub.cost_min, 'cost_max': pub.cost_max, 'photo': photos, 'tag_lifehack_lifesphere': tag_lifehack_lifesphere, })

    title = 'Отредактирвать публикацию'
    return render(request, 'publicationapp/create_new_or_update.html', {'title': title, 'form': form, })

class Saved(ListView):
    model = SavedPubs
    template_name = 'publicationapp/saved.html'
    context_object_name = 'pubs'

    def get_queryset(self):
        return SavedPubs.objects.filter(saver_id=self.request.user).order_by('-when')

    def get_context_data(self, **kwargs):
        context = super(Saved, self).get_context_data(**kwargs)
        # у меня не получилось получить только некоторые записи тегов, пришось всей кучей. но работает :)
        # saved_pubs = SavedPubs.objects.filter(saver_id=self.request.user)
        # publications = Publication.objects.filter(id=SavedPubs.objects.filter(saver_id=self.request.user))
        # # какого фига publications queryset получаают, а у PubHasTags точно так же не получается?
        # print(saved_pubs)
        # print(str(publications))
        # print(PubHasTags.objects.filter(pub_id__in=publications))

        context.update({
            'pub_has_tags': PubHasTags.objects.filter(),
        })
        return context

def toggle_saved(request, pk):
    if request.is_ajax():
        duplicate = SavedPubs.objects.filter(saver_id=request.user, pub_id=pk)

        if not duplicate:
            record = SavedPubs.objects.create(saver_id=request.user, pub_id=Publication.objects.get(id=pk))
            record.save()
            result = 1
        else:
            duplicate.delete()
            result = 0

        # context = {
        #     'user': request.user,
        #     'news_item': NewsItem.objects.get(pk=pk)
        # }

        # result = render_to_string('newsapp/includes/likes_block.html', context)
        return JsonResponse({'result': result})

class RepairsWatch(ListView):
    model = Publication
    template_name = 'publicationapp/repairs.html'
    context_object_name = 'pubs'

    def get_queryset(self):
        return Publication.objects.filter(role=11)

class DesignsWatch(ListView):
    model = Publication
    template_name = 'publicationapp/designs.html'
    context_object_name = 'pubs'

    def get_queryset(self):
        return Publication.objects.filter(role=21)

def filter_lifehacks(request):
    sphera = request.POST.getlist('style_design', '')
    fltr_cost_min = request.POST.get('cost_mini', '')
    fltr_cost_max = request.POST.get('cost_max', '')
    return HttpResponse('sphera: '+ str(sphera) +', fltr_cost_min:'+ fltr_cost_min +', fltr_cost_max:'+ fltr_cost_max)

class LifehacksWatch(ListView):
    model = Publication
    # model = PubHasTags
    template_name = 'publicationapp/lifehacks.html'
    context_object_name = 'pubs'

    def get_queryset(self):
        return Publication.objects.filter(role=31)

    def get_context_data(self, **kwargs):
        context = super(LifehacksWatch, self).get_context_data(**kwargs)
        publications = Publication.objects.filter(role=31)

        context.update({
            'pub_has_tags': PubHasTags.objects.filter(pub_id__in=publications),
            # 'tags_for_filter': TagName.objects.filter(id__gt=3000000).filter(id__lt=3999999)
        })
        return context

class FilterLifehacks(ListView):
    model = Publication
    template_name = 'publicationapp/lifehacks_filtered.html'
    context_object_name = 'pubs'
    allow_empty = False
    # slug_url_kwarg = 'your_lovely_slug' это памятка на будущее: чтобы класс типа View искал не slug (это стандартно), а то, что хочется - your_lovely_slug. касательно pk: pk_url_kwarg = your_lovely_pk

    def get_queryset(self):
        return Publication.objects.filter(role=31)

    def get_context_data(self, **kwargs):
        context = super(FilterLifehacks, self).get_context_data(**kwargs)
        publications = Publication.objects.filter(role=31)

        # request = self.kwargs['request']
        if self.request.method == 'GET':
            sphera = self.request.GET.getlist('style_design', '')
            fltr_cost_min = self.request.GET.get('cost_mini', '')
            fltr_cost_max = self.request.GET.get('cost_max', '')
            if sphera != '':
                filter_tag = PubHasTags.objects.filter(tag_id__in=sphera)
            if fltr_cost_min != '':
                publications = publications.filter(cost_min__gte=fltr_cost_min)
            if fltr_cost_max != '':
                publications = publications.filter(cost_max__lte=fltr_cost_max)
        else:
            filter_tag = PubHasTags.objects.all()

        context.update({
            'filter_tag': filter_tag,
            'pubs': publications,
            'pub_has_tags': PubHasTags.objects.filter(pub_id__in=publications),
        })
        return context

class PubWatchOne(ListView):
    model = Publication
    template_name = 'publicationapp/pub_one.html'
    context_object_name = 'pub'
    allow_empty = False # сделать ответ на случай, если публикации с введённым id не существует

    def get_queryset(self):
        return Publication.objects.get(id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(PubWatchOne, self).get_context_data(**kwargs)
        # publications = Publication.objects.get(id=self.kwargs['pk'])

        context.update({
            'pub_has_tags': PubHasTags.objects.filter(pub_id=self.kwargs['pk']),
            'photos': PubPhotos.objects.filter(id_pub=self.kwargs['pk']),
        })
        return context
