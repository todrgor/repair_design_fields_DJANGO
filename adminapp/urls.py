from django.urls import path
import adminapp.views as adminapp
import authapp.views as authapp
import publicationapp.views as publicationapp
import mainapp.views as mainapp

app_name = 'adminapp'

urlpatterns = [
    path('', adminapp.StartPanel.as_view(), name='main'),

    path('tags_and_tag_categories/', adminapp.TagsAndTagCategories, name='tags_and_tag_categories'),
    path('letters_to_support/', adminapp.LettersToSupport, name='letters_to_support'),
    path('pubs/', adminapp.PubList.as_view(), name='pubs'),
    path('users/', adminapp.UserList.as_view(), name='users'),
    path('user/<int:pk>/', adminapp.UserIndividual, name='user_individual'),
    path('create/user/', authapp.CreateAccount, name='user_create_new'),
    path('journal/', adminapp.JournalList.as_view(), name='journal'),

    path('new_complaint/', adminapp.NewComplaint, name='new_complaint'),
]
