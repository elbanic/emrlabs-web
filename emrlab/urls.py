from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('lab1/', views.lab1, name='lab1'),
    path('lab2/', views.lab2, name='lab2'),
    path('lab3/', views.lab3, name='lab3'),
    path('lab4/', views.lab4, name='lab4'),
    path('finish/', views.finish, name='finish'),

]