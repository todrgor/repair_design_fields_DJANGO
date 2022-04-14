from django.contrib import admin

from .models import Publication, PubPhotos, PubTypes, PubHasTags, TagName

admin.site.register(Publication)
admin.site.register(PubPhotos)
admin.site.register(PubTypes)
admin.site.register(PubHasTags)
admin.site.register(TagName)
