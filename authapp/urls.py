from django.urls import path
import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    path('getNotifications/<pk>/', authapp.toggle_get_noti_from_author, name='toggle_get_noti_from_author'),
    path('NewNotiWereSeen/<pk>/', authapp.new_noti_were_seen, name='new_noti_were_seen'), 
    path('login/', authapp.UserLoginView.as_view(), name='login'),
    path('logout/', authapp.UserLogoutView.as_view(), name='logout'),
    path('register/', authapp.UserRegisterView.as_view(), name='register'),
    path('one/<pk>/', authapp.AccountOneWatch.as_view(), name='account_one'),
    path('settings/<pk>/', authapp.UpdateAccount, name='settings'),
]
