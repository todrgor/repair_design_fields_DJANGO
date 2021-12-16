from django.contrib import admin

from .models import *

admin.site.register(User)
admin.site.register(UserRoles)
admin.site.register(UserSubscribes)
admin.site.register(ExpertInfo)
admin.site.register(SavedPubs)
admin.site.register(SeenPubs)
admin.site.register(Notifications)
admin.site.register(ContactingSupport)
admin.site.register(ContactingSupportTypes)
