from django.urls import path, include
from . import views
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'Usuario', views.UsuarioViewSet)
router.register(r'UsuarioRespuesta', views.UsuarioRespuestaViewSet)
router.register(r'UsuarioTextoPregunta', views.UsuarioTextoPreguntaViewSet)


urlpatterns = [
    path('', views.login),
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('reportes/', views.reportes, name='reportes'),
    path('formulario/', views.formulario, name='formulario'),
    
    #Respuestas
    path('respuestas/', views.respuestasHome, name='respuestasHome'),
    path('datosPerfil/', views.datosPerfil, name='datosPerfil'),
    path('datosPreguntas/', views.datosPreguntas, name='datosPreguntas'),
    path('datosTextoPreguntas/', views.datosTextoPreguntas, name='datosTextoPreguntas'),
    
    #Preguntas
    path('listarPreguntas/', views.listarPreguntas, name='listarPreguntas'),
    path('modificarPregunta/<id>/', views.modificarPregunta, name='modificarPregunta'),
    path('eliminarPregunta/<id>/', views.eliminarPregunta, name='eliminarPregunta'),
    path('crearPregunta/', views.crearPregunta, name='crearPregunta'),
    #Api
    path('api/v1/', include(router.urls)),    

]