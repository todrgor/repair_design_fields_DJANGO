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
	path('', mainapp.main),
	path('repairs/', mainapp.repairs),
	path('designs/', mainapp.designs),
	path('lifehacks/', mainapp.lifehacks),
	path('saved/', mainapp.saved),
	path('account/', mainapp.account),
	path('account_edit/', mainapp.account_edit),
	path('pub_one/', mainapp.pub_one),
	path('pub_create_new/', mainapp.pub_create_new),
	path('pub_edit/', mainapp.pub_edit),
	path('support/', mainapp.support),
	path('become_an_author/', mainapp.become_an_author),
	path('become_a_teammemder/', mainapp.become_a_teammemder),
	path('help/', mainapp.help),
	path('adminRDF/', mainapp.adminRDF), 

	path('admin/', admin.site.urls),
]
