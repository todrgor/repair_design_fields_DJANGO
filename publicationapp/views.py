from django.views.generic.list import ListView

from django.shortcuts import render
from authapp.models import *
from publicationapp.models import *
import mimetypes

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
        tags = {}
        for p in publications:
            pub_has_tags = PubHasTags.objects.filter(pub_id=p)
            for tag in pub_has_tags:
                tags.apdate({
                    str(p.id): 
                })
                tags[p.id][tag_id] = tag.tag_id.tag_name

        tags = (
            p_id1 = (
                filterName1, filterName2
            )
            p_id1 = (
                filterName1, filterName2, filterName3
            )
        )

        context.update({
            'pub_has_tags': PubHasTags.objects.filter(pub_id__in=publications),
            'tags': TagName.objects.filter(id__gt=3000000).filter(id__lt=3999999), # у меня не получилось как с pub_has_tags pub_id__in=pubs
        })
        return context
