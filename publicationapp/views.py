from django.views.generic.list import ListView
from django.http import HttpResponse
# from django.views.generic.detail import DetailView

from django.shortcuts import render
from authapp.models import *
from publicationapp.models import *
from .forms import *
# import mimetypes

def CreateNewPub(request):
    form = PubForm()
    if request.method == 'POST':
        form = PubForm(request.POST)
        if form.is_valid():
            pub = request.POST
            print(pub['role'])
        else:
            print('форма не валидная')
    title = 'Создать публикацию'
    return render(request, 'publicationapp/create_new_or_update.html', {'title': title, 'form': form, })


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
