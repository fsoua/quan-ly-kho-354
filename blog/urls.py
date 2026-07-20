from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('second/', views.second, name='second'),
    path('greet/<str:name>/<int:age>', views.greet, name='greet'),
    path('insert_computer', views.insert_computer, name='insert_computer')
]