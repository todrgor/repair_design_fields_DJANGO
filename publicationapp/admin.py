from django.contrib import admin

from .models import Publication, PubTypes, TagCategory, Tag, PubPhotos, PubHasTags, TagName

admin.site.register(Publication)
admin.site.register(PubTypes)
admin.site.register(TagCategory)
admin.site.register(Tag)

admin.site.register(PubPhotos)
admin.site.register(PubHasTags)
admin.site.register(TagName)
