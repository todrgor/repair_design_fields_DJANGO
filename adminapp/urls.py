from django.urls import path
import adminapp.views as adminapp

app_name = 'adminapp' 

urlpatterns = [
    path('', adminapp.main, name='main'),
    path('edit/account/<pk>/', adminapp.EditAccount.as_view(), name='edit_account'),
    path('edit/pub/<pk>/', adminapp.EditPub.as_view(), name='edit_pub'),
    path('create/account/<pk>/', adminapp.CreateNewAccount.as_view(), name='create_new_account'),
    path('create/pub/<pk>/', adminapp.CreateNewPub.as_view(), name='create_new_pub'),
]
