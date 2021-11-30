from django.urls import path
import authapp.views as authapp

app_name = 'authapp' 

urlpatterns = [
    path('login/', authapp.Login.as_view(), name='login'),
    path('logout/', authapp.Logout.as_view(), name='logout'),

    path('<pk>/', authapp.AccountOneWatch.as_view(), name='account_watch'),
    path('saved/', authapp.Saved.as_view(), name='saved'),
    path('settings/', authapp.Settings.as_view(), name='settings'),
    # по логике, account edit = account settings!
    # path('edit/', supportapp.AccountEdit.as_view(), name='account_edit'),
]
