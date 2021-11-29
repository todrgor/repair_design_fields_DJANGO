from django.contrib import admin

from .models import User, UserRoles, UserSubscribes, ExpertInfo, SavedPubs, SeenPubs

admin.site.register(User)
admin.site.register(UserRoles)
admin.site.register(UserSubscribes)
admin.site.register(ExpertInfo)
admin.site.register(SavedPubs)
admin.site.register(SeenPubs)
