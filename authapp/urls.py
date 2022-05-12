from django.views.generic.base import RedirectView
from django.urls import path
import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    path('', RedirectView.as_view(url='/', permanent=False), name='index'),

    path('<int:pk>/', authapp.AccountOneWatch.as_view(), name='one'),
    path('<int:pk>/settings/', authapp.UpdateAccount, name='settings'),
    path('<int:pk>/settings/change_password/', authapp.ChangePassword, name='change_password'),
    path('<int:pk>/delete/', authapp.DeleteAccount, name='delete'),

    path('<int:pk>/toggleNotifications/', authapp.toggle_get_noti_from_author, name='toggle_get_noti_from_author'),
    path('<int:pk>/NewNotiWereSeen/', authapp.new_noti_were_seen, name='new_noti_were_seen'),
]
