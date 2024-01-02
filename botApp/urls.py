from django.urls import path
from . import views



urlpatterns = [
    path('', views.login),
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),

]