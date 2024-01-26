from datetime import datetime
from io import BytesIO
import base64
import matplotlib.pyplot as plt
import requests

from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import connection
from django.shortcuts import render, redirect

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets

from .forms import *
from .models import *
from .serializer import *


def generar_grafico_respuestas_por_dia():
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT DATE(Fecha_Ingreso), COUNT(*) FROM botApp_usuario GROUP BY DATE(Fecha_Ingreso)"
        )
        resultados = cursor.fetchall()

    fechas = []
    cantidades = []

    for resultado in resultados:
        fecha, cantidad = resultado
        fechas.append(datetime.strftime(fecha, "%Y-%m-%d"))
        cantidades.append(cantidad)

    plt.plot(fechas, cantidades, marker="o", linestyle="-", color="blue")
    plt.xlabel("Fecha de Respuesta")
    plt.ylabel("Número de Respuestas")
    plt.title("Respuestas por Día")

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()

    imagen_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return imagen_base64


@login_required
def home(request):
    return render(request, "home.html")


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("home")
        else:
            return render(request, "registration/login.html")

    return render(request, "registration/login.html")


# Base de datos
@login_required
def database(request):
    Datos = Usuario.objects.all().order_by("-Fecha_Ingreso")
    data = {
        "Datos": Datos,
    }
    return render(request, "database.html", data)


# Reportes
@login_required
def reportes(request):
    data = {
        "imagen_base64_ingresos": generar_grafico_respuestas_por_dia(),
    }
    return render(request, "reportes.html", data)


# Formulario
@login_required
def formulario(request):
    data = {
        "formUsuario": UsuarioForm(),
        "preguntas": Pregunta.objects.all(),
        "usuarios": User.objects.all(),
    }

    if request.method == "POST":
        form_usuario = UsuarioForm(request.POST)

        if form_usuario.is_valid():
            form_usuario.instance.id_usuario = request.POST.get("id_usuario")
            usuario = form_usuario.save()

            for pregunta in data["preguntas"]:
                respuesta = request.POST.get(f"pregunta_{pregunta.id}")
                opc_respuesta = OPC_Respuesta(
                    id_pregunta=pregunta, OPC_Respuesta=respuesta
                )
                opc_respuesta.save()
                respuesta_usuario = RespuestaUsuario(
                    id_usuario=usuario,
                    id_pregunta=pregunta,
                    id_opc_respuesta=opc_respuesta,
                )
                respuesta_usuario.save()

            messages.success(request, "Datos guardados correctamente")
            form_usuario = UsuarioForm()
            return redirect(to="home")

        else:
            print(form_usuario.errors)
            messages.error(
                request,
                "La persona debe tener más de 18 años y haber nacido después de 1930.",
            )
            form_usuario = UsuarioForm()

    return render(request, "formulario.html", data)


# --------------------- Preguntas --------------------- #
@login_required
def preguntasHome(request):
    return render(request, "preguntas/preguntasHome.html")


# Listar Preguntas
@login_required
def listarPreguntas(request):
    Preguntas = Pregunta.objects.all()
    data = {
        "preguntas": Preguntas,
    }
    return render(request, "preguntas/listarPreguntas.html", data)


# Modificar Pregunta
@login_required
def modificarPregunta(request, id):
    Preguntas = Pregunta.objects.get(id=id)
    data = {"form": PreguntaForm(instance=Preguntas)}

    if request.method == "POST":
        formulario = PreguntaForm(
            data=request.POST, instance=Preguntas, files=request.FILES
        )
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado Correctamente")
            return redirect(to="listarPreguntas")
        data["form"] = formulario

    return render(request, "preguntas/modificarPreguntas.html", data)


# Eliminar Pregunta
@login_required
def eliminarPregunta(request, id):
    Preguntas = Pregunta.objects.get(id=id)
    Preguntas.delete()
    messages.success(request, "Eliminado Correctamente")
    return redirect(to="listarPreguntas")


# Crear Pregunta
@login_required
def crearPregunta(request):
    data = {"form": PreguntaForm()}

    if request.method == "POST":
        formulario = PreguntaForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Pregunta Creada Correctamente")
        else:
            data["form"] = formulario

    return render(request, "preguntas/crearPreguntas.html", data)


# --------------------- Api --------------------- #

#Usuario
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    
#RespuestaUsuario
class UsuarioRespuestaViewSet(viewsets.ModelViewSet):
    queryset = UsuarioRespuesta.objects.all()
    serializer_class = UsuarioRespuestaSerializer
    


# --------------------- Api --------------------- #