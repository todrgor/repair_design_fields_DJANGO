from django.views.generic.base import RedirectView
from django.urls import path
import publicationapp.views as publicationapp
import mainapp.views as mainapp

app_name = 'publicationapp'

urlpatterns = [
    path('', RedirectView.as_view(url='/', permanent=False), name='index'),

    path('create/', publicationapp.CreateNewPub, name='create_new'),
    path('<int:pk>/', publicationapp.PubWatchOne.as_view(), name='one'),
    path('<int:pk>/delete/', publicationapp.DeletePub, name='delete'),
    path('<int:pk>/edit/', publicationapp.UpdatePub, name='edit'),

    path('<int:pk>/toggle_saved/', publicationapp.toggle_saved, name='toggle_saved'),
    path('<int:pk>/set_seen/', publicationapp.set_seen, name='set_seen'),
    path('<int:pk>/change_shared_count/', publicationapp.change_shared_count, name='change_shared_count'),
    path('get_filtered_pubs_count/', publicationapp.get_filtered_pubs_count, name='get_filtered_pubs_count'),
]
