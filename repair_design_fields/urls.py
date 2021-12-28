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
from django.conf.urls.static import static
from repair_design_fields import settings
from django.contrib import admin
from django.urls import path, include
import mainapp.views as mainapp
import authapp.views as authapp

urlpatterns = [
    path('', mainapp.main, name='main'),
    path('pub/', include('publicationapp.urls', namespace='pub')),
	# path('support/', include('supportapp.urls', namespace='support')),
	path('account/', include('authapp.urls', namespace='auth')),
    path('admin/', include('adminapp.urls', namespace='admin_mine')),
	# path('adminRDF/', mainapp.adminRDF, name='adminRDF'),
    path('search/', authapp.Search, name='search'),

	path('adminDJANGO/', admin.site.urls),
	# path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
