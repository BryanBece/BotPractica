from django.urls import path
from . import views



urlpatterns = [
    path('', views.login),
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('database/', views.database, name='database'),
    path('reportes/', views.reportes, name='reportes'),
    path('formulario/', views.formulario, name='formulario'),
    #Preguntas
    path('preguntas/', views.preguntasHome, name='preguntas'),
    path('listarPreguntas/', views.listarPreguntas, name='listarPreguntas'),
    path('modificarPregunta/<id>/', views.modificarPregunta, name='modificarPregunta'),
    path('eliminarPregunta/<id>/', views.eliminarPregunta, name='eliminarPregunta'),
    path('crearPregunta/', views.crearPregunta, name='crearPregunta'),

]