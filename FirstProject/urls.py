"""FirstProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path,include
from mainapp.views import Home,About
from django.conf import settings
from django.conf.urls.static import static
from mainapp.views_helper import SearchView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Home,name='home'),
    path('users/',include('accounts.urls',namespace="users")),
    path('post/',include('mainapp.urls',namespace='post')),
    path('about/',About,name='about'),
    path('search/',SearchView,name='search'),
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
