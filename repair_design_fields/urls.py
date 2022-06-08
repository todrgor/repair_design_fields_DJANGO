from django.conf.urls.static import static
from repair_design_fields import settings
from django.contrib import admin
from django.urls import path, include
import mainapp.views as mainapp
import authapp.views as authapp
import publicationapp.views as publicationapp
import authapp.views as authapp
from ckeditor_uploader import views as ckeditor_views

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

urlpatterns = [
    path('', mainapp.main, name='main'),

    path('pub/', include('publicationapp.urls', namespace='pub')),
    path('designs/', publicationapp.DesignsWatch.as_view(), name='designs'),
    path('repairs/', publicationapp.RepairsWatch.as_view(), name='repairs'),
    path('lifehacks/', publicationapp.LifehacksWatch.as_view(), name='lifehacks'),
    path('saved/', publicationapp.Saved.as_view(), name='saved'),

    path('become_a_teammemder/', authapp.BecomeATeammember, name='become_a_teammemder'),
    path('become_an_author/', authapp.BecomeAnAuthor, name='become_an_author'),
    path('send_to_support/', authapp.SendToSupport, name='send_to_support'),

	path('account/', include('authapp.urls', namespace='auth')),
    path('register/', authapp.UserRegisterView.as_view(), name='register'),
    path('login/', authapp.UserLoginView.as_view(), name='login'),
    path('logout/', authapp.UserLogout, name='logout'),
    path('search/', authapp.Search, name='search'),

    path('admin/', include('adminapp.urls', namespace='admin_mine')),
	path('admin/django/', admin.site.urls, name='admin_django'),

    # path('ckeditor/', include('ckeditor_uploader.urls')),     #   STANDART
    path('ckeditor/upload/', login_required(ckeditor_views.upload), name='ckeditor_upload'),
    path('ckeditor/browse/', never_cache(login_required(ckeditor_views.browse)), name='ckeditor_browse'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
