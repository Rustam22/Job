from django.urls import path

from . import views

urlpatterns = [
    path('hello/', views.hello, name='hello'),
    path('template/', views.helloTemplate, name='helloTemplate'),
    path('classTemplate/', views.HelloTemplate.as_view(), name='helloClassTemplate'),
]
