"""repair_design_fields URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import mainapp.views as mainapp

urlpatterns = [
path('profile/', ),
    path('', mainapp.main, name='main'),
	path('repairs/', include('publicationapp.urls', namespace='repair')),
	path('designs/', include('publicationapp.urls', namespace='designs')),
	path('lifehacks/', include('publicationapp.urls', namespace='lifehacks')),
	path('pub/', include('publicationapp.urls', namespace='pub')),
    # path('pub/create/', mainapp.pub_create_new, name='pub_create_new'),
	# path('pub/edit/', mainapp.pub_edit, name='pub_edit'),
    path('saved/', include('authapp.urls', namespace='saved')),
	path('account/', include('authapp.urls', namespace='account')),
	# path('account/edit/', mainapp.account_edit, name='account_edit'),
	# path('account/settings/', mainapp.account_edit, name='account_edit'),
	path('support/', include('adminapp.urls', namespace='support')),
	# path('support/become_an_author/', include('adminapp.urls', namespace='become_an_author')),
	# path('support/become_a_teammemder/', include('adminapp.urls', namespace='become_a_teammemder')),
	# path('support/help/', include('adminapp.urls', namespace='help')),
	# path('support/', include('adminapp.urls', namespace='support')),
	# path('adminRDF/', mainapp.adminRDF, name='adminRDF'),
	path('admin/', include('adminapp.urls', namespace='admin')),
	# path('admin/', mainapp.adminRDF, name='adminRDF'),

	path('adminDJANGO/', admin.site.urls),
	# path('admin/', admin.site.urls),
]
