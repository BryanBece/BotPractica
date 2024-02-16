from django.urls import path, include
from . import views
from rest_framework import routers
from .views import *


router = routers.DefaultRouter()
router.register(r'Usuario', views.UsuarioViewSet)
router.register(r'UsuarioRespuesta', views.UsuarioRespuestaViewSet)
router.register(r'UsuarioTextoPregunta', views.UsuarioTextoPreguntaViewSet)
router.register(r'MensajeContenido', views.MensajeContenidoViewSet)

urlpatterns = [
    path('', views.login),
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('reportes/', views.reportes, name='reportes'),
    path('formulario/', views.formulario, name='formulario'),
    
    # Respuestas
    path('respuestas/', views.respuestasHome, name='respuestasHome'),
    path('datosPerfil/', views.datosPerfil, name='datosPerfil'),
    path('datosPreguntas/', views.datosPreguntas, name='datosPreguntas'),
    path('datosTextoPreguntas/', views.datosTextoPreguntas, name='datosTextoPreguntas'),
    
    # Preguntas
    path('listarPreguntas/', views.listarPreguntas, name='listarPreguntas'),
    path('modificarPregunta/<id>/', views.modificarPregunta, name='modificarPregunta'),
    path('eliminarPregunta/<id>/', views.eliminarPregunta, name='eliminarPregunta'),
    path('crearPregunta/', views.crearPregunta, name='crearPregunta'),

    # Descargar Excel
    path('descargar_excel/', views.descargar_excel, name='descargar_excel'),

    # API
    path('api/v1/', include(router.urls)),
    
    path('apiHome/', apiHome, name='apiHome'),
    path('obtener-id/', ObtenerID.as_view(), name='obtener_id'),    
    path('api_usuario/', UsuarioAPIView.as_view(), name='api_usuario'),
    path('api_pregunta/', UsuarioTextoPreguntaAPIView.as_view(), name='api_pregunta'),
    path('api_respuesta/', UsuarioRespuestaAPIView.as_view(), name='api_respuesta'),
    path('api_mensaje/', MensajeContenidoAPIView.as_view(), name='api_mensaje'),
]