from django.urls import path
import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    path('login/', authapp.UserLoginView.as_view(), name='login'),
    path('logout/', authapp.UserLogoutView.as_view(), name='logout'),
    path('register/', authapp.UserRegisterView.as_view(), name='register'),

    # path('login/', authapp.login, name='login'),
    # path('logout/', authapp.logout, name='logout'),

    # path('<pk>/', authapp.AccountOneWatch.as_view(), name='account_watch'),
    # path('saved/', authapp.Saved.as_view(), name='saved'),
    # path('settings/', authapp.Settings.as_view(), name='settings'),
    # по логике, account edit = account settings!
    # path('edit/', supportapp.AccountEdit.as_view(), name='account_edit'),
]
