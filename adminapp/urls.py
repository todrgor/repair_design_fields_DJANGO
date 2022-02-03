# from django.urls import path
# import adminapp.views as adminapp
#
# app_name = 'adminapp'
#
# urlpatterns = [
#     path('', adminapp.main, name='main'),
#     path('edit/account/<pk>/', adminapp.EditAccount.as_view(), name='edit_account'),
#     path('edit/pub/<pk>/', adminapp.EditPub.as_view(), name='edit_pub'),
#     path('create/account/<pk>/', adminapp.CreateNewAccount.as_view(), name='create_new_account'),
#     path('create/pub/<pk>/', adminapp.CreateNewPub.as_view(), name='create_new_pub'),
# ]

from django.urls import path
import adminapp.views as adminapp
import authapp.views as authapp
import publicationapp.views as publicationapp
import mainapp.views as mainapp

app_name = 'adminapp'

urlpatterns = [
    path('', adminapp.StartPanel.as_view(), name='main'),
    path('letters_to_support/', adminapp.LettersToSupport, name='letters_to_support'),
    path('pubs/', adminapp.PubList.as_view(), name='pubs'),
    path('users/', adminapp.UserList.as_view(), name='users'),
    path('users/create/', authapp.CreateAccount, name='user_create_new'),
    path('pub/create/', publicationapp.CreateNewPub, name='pub_create_new'),
    path('pub/delete/<pk>/', publicationapp.DeletePub, name='pub_delete'),
    path('pub/update/<pk>/', publicationapp.UpdatePub, name='pub_update'),

    path('new_complaint/', adminapp.NewComplaint, name='new_complaint'),
]
