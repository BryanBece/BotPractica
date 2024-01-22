from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'Prueba', views.PruebaViewSet)
router.register(r'Usuario', views.UsuarioViewSet)
router.register(r'RespuestaUsuario', views.RespuestaUsuarioViewSet)


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
    #Api
    path('api/v1/', include(router.urls)),
    

]