from django.contrib import admin

from .models import *

admin.site.register(Publication)
admin.site.register(PubTypes)
admin.site.register(SavedPubs)
admin.site.register(SeenPubs)
admin.site.register(TagCategory)
admin.site.register(Tag)
