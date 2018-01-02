from django.urls import path
from . import views


urlpatterns = [
    path('', views.base, name='base'),
    path('registration/', views.signup, name='base'),
]