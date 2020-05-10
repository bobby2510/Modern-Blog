from django.shortcuts import render
from django.urls import path
from accounts.views import RegisterView,MyLoginView,MyLogoutView,ProfileView,EditProfielView
app_name='accounts'
urlpatterns=[
    path('register/',RegisterView,name='register'),
    path('login/',MyLoginView.as_view(),name='login'),
    path('logout/',MyLogoutView.as_view(),name='logout'),
    path('<str:uname>/',ProfileView,name='profile'),
    path('<str:uname>/edit',EditProfielView,name='editprofile'),
]