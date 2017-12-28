from django.urls import path
from . import views


urlpatterns = [
    path('', views.base, name='base'),
    path('userForm/', views.userForm, name='userForm'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('registration/', views.registration, name='registration'),
]