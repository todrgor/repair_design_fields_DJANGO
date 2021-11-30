from django.urls import path
import publicationapp.views as publicationapp

app_name = 'publicationapp'

urlpatterns = [
    path('', publicationapp.main, name='main'),
    path('<pk>/', publicationapp.PubOneWatch.as_view(), name='pub_watch'),
    path('create/', publicationapp.CreateNew.as_view(), name='create_new'),
    path('<pk>/edit/', publicationapp.PubOneEdit.as_view(), name='pub_edit'),
    path('repairs/', publicationapp.RepairsWatch.as_view(), name='repairs'),
    path('designs/', publicationapp.DesignsWatch.as_view(), name='designs'),
    path('lifehacks/', publicationapp.LifehacksWatch.as_view(), name='lifehacks'),
]
