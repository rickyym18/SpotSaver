from django import urls
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.about),
    path('form', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('main', views.main),
    path('place/<int:spot_id>', views.placeprofile),
    path("creating", views.create_spot),
    path("adding", views.home_adding_spot),
    path("back", views.back_home),
    path('delete/<int:id>', views.delete)
]
