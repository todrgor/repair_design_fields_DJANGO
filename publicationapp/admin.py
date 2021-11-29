from django.contrib import admin

from .models import Publication, PubPhotos, PubRoles, PubHasTags, TagName

admin.site.register(Publication)
admin.site.register(PubPhotos)
admin.site.register(PubRoles)
admin.site.register(PubHasTags)
admin.site.register(TagName)
