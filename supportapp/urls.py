from django.urls import path
import supportapp.views as supportapp

app_name = 'supportapp' 

urlpatterns = [
    path('', supportapp.main, name='main'),
    path('become_an_author/', supportapp.BecomeAnAuthor.as_view(), name='become_an_author'),
    path('become_a_teammemder/', supportapp.BecomeATeamMember.as_view(), name='become_a_teammemder'),
    path('help/', supportapp.Help.as_view(), name='help'),
]
