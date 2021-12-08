from django.urls import path
import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    path('login/', authapp.UserLoginView.as_view(), name='login'),
    path('logout/', authapp.UserLogoutView.as_view(), name='logout'),
    path('register/', authapp.UserRegisterView.as_view(), name='register'),
    path('one/<pk>/', authapp.AccountOneWatch.as_view(), name='account_one'),
    path('settings/<pk>/', authapp.UpdateAccount, name='settings'),


    # path('saved/', authapp.Saved.as_view(), name='saved'),
]
