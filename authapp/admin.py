from django.contrib import admin

from .models import *

admin.site.register(User)
admin.site.register(UserRoles)
admin.site.register(ExpertInfo)
admin.site.register(ActionTypes)
admin.site.register(NotificationsNewTable)
admin.site.register(JournalActions)
admin.site.register(ContactingSupport)
admin.site.register(ContactingSupportPhotos)
admin.site.register(ContactingSupportTypes)

#   это вскоре убрать нужно
admin.site.register(Notifications)
