from django.urls import path
import publicationapp.views as publicationapp
import mainapp.views as mainapp

app_name = 'publicationapp'

urlpatterns = [
    path('', mainapp.main, name='main'),
    path('one/<pk>/', publicationapp.PubWatchOne.as_view(), name='pub_one'),
    path('create/', publicationapp.CreateNewPub, name='create_new'),
    # path('one/<pk>/edit/', publicationapp.PubOneEdit.as_view(), name='pub_edit'),
    path('repairs/', publicationapp.RepairsWatch.as_view(), name='repairs'),
    path('designs/', publicationapp.DesignsWatch.as_view(), name='designs'),
    path('lifehacks/', publicationapp.LifehacksWatch.as_view(), name='lifehacks'),
    path('lifehacks/filter/', publicationapp.FilterLifehacks.as_view(), name='filter_lifehacks'),
]
