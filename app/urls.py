from django.urls import path
from . import views

urlpatterns=[
    path('', views.home, name='home'),
    path('room/<str:pk>', views.room, name='room'),
    path('create-room', views.createRoom, name='create-room'),
    path('update_room/<str:pk>', views.update_room,name='update_room'),
    path('delete_room/<str:pk>', views.delete_room, name='delete_room'),
    path('login', views.loginPage, name='login'),
    path('logout', views.logoutPage, name='logout'),
    path('register', views.registerPage, name='register')
]