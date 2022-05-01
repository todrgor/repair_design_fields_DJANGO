from django.contrib import admin

from .models import Publication, PubTypes, TagCategory, Tag, PubPhotos

admin.site.register(Publication)
admin.site.register(PubTypes)
admin.site.register(TagCategory)
admin.site.register(Tag)

admin.site.register(PubPhotos)
