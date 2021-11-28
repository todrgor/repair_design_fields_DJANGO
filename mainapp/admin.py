from django.contrib import admin

from .models import User
from .models import UserRoles
from .models import UserSubscribes
from .models import ExpertInfo
from .models import Publication
from .models import PubRoles
from .models import SavedPubs
from .models import SeenPubs
from .models import PubHasTags
from .models import TagName

admin.site.register(User)
admin.site.register(UserRoles)
admin.site.register(UserSubscribes)
admin.site.register(ExpertInfo)
admin.site.register(Publication)
admin.site.register(PubRoles)
admin.site.register(SavedPubs)
admin.site.register(SeenPubs)
admin.site.register(PubHasTags)
admin.site.register(TagName)
