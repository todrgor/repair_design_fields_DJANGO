from django.urls import path
import publicationapp.views as publicationapp
import mainapp.views as mainapp

app_name = 'publicationapp'

urlpatterns = [
    path('', mainapp.main, name='main'),
    path('saved/', publicationapp.Saved.as_view(), name='saved'),
    path('make_saved/<pk>/', publicationapp.toggle_saved, name='toggle_saved'),
    path('set_seen/<pk>/', publicationapp.set_seen, name='set_seen'),
    path('change_shared_count/<pk>/', publicationapp.change_shared_count, name='change_shared_count'),
    path('get_filtered_pubs_count/', publicationapp.get_filtered_pubs_count, name='get_filtered_pubs_count'),
    path('one/<pk>/', publicationapp.PubWatchOne.as_view(), name='pub_one'),
    path('create/', publicationapp.CreateNewPub, name='create_new'),
    path('delete/<pk>/', publicationapp.DeletePub, name='delete'),
    path('one/<pk>/edit/', publicationapp.UpdatePub, name='pub_edit'),
    path('repairs/', publicationapp.RepairsWatch.as_view(), name='repairs'),
    path('designs/', publicationapp.DesignsWatch.as_view(), name='designs'),
    path('lifehacks/', publicationapp.LifehacksWatch.as_view(), name='lifehacks'),
]
