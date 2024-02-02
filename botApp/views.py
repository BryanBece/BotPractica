import matplotlib
matplotlib.use('Agg')

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
from django.db.models import Count


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets

from .forms import *
from .models import *
from .serializer import *


    
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

# --------------------- Respuestas de Usuario --------------------- #

#Home
@login_required
def respuestasHome(request):
    return render(request, "respuestas/respuestasHome.html")


# Base de datos
@login_required
def datosPerfil(request):
    Datos = Usuario.objects.all().order_by("-Fecha_Ingreso")
    data = {
        "Datos": Datos,
    }
    return render(request, "respuestas/datosPerfil.html", data)

@login_required
def datosPreguntas(request):
    Datos = UsuarioRespuesta.objects.all().order_by("-fecha_respuesta")
    data = {
        "Datos": Datos,
    }
    return render(request, "respuestas/datosPreguntas.html", data)

@login_required
def datosTextoPreguntas(request):
    Datos = UsuarioTextoPregunta.objects.all().order_by("-fecha_pregunta")
    data = {
        "Datos": Datos,
    }
    return render(request, "respuestas/datosPreguntasEspecialistas.html", data)


# --------------------- Reporteria --------------------- #

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

def generar_grafico_personas_por_genero():
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT Genero_Usuario_id, COUNT(*) FROM botApp_usuario GROUP BY Genero_Usuario_id"
        )
        resultados = cursor.fetchall()

    generos = []
    cantidades = []

    for resultado in resultados:
        genero_id, cantidad = resultado
        genero = Genero.objects.get(id=genero_id)
        generos.append(genero.OPC_Genero)
        cantidades.append(cantidad)

    # Crear gráfico de dispersión con diferentes colores para cada punto
    colores = {'Masculino': 'blue', 'Femenino': 'pink', 'Otro': 'green'}
    plt.scatter(generos, cantidades, c=[colores[genero] for genero in generos], marker='o')

    # Crear líneas desde cada punto hasta el eje y (punto 0)
    for genero, cantidad in zip(generos, cantidades):
        plt.plot([genero, genero], [0, cantidad], color=colores[genero], linestyle='--')

    plt.xlabel("Género")
    plt.ylabel("Número de Personas")
    plt.title("Ingresos por Género")

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()

    imagen_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return imagen_base64
    
def generar_graficos_genero_por_comuna():
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT c.Nombre_Comuna, g.OPC_Genero, COUNT(*) "
            "FROM botApp_usuario u "
            "JOIN botApp_comuna c ON u.Comuna_Usuario_id = c.id "
            "JOIN botApp_genero g ON u.Genero_Usuario_id = g.id "
            "GROUP BY c.Nombre_Comuna, g.OPC_Genero"
        )
        resultados = cursor.fetchall()

    # Crear gráficos circulares para cada comuna
    imagenes_base64 = []

    comunas = set(result[0] for result in resultados)
    for comuna in comunas:
        generos = {'Masculino': 0, 'Femenino': 0, 'Otro': 0}
        total_personas = 0

        # Contar la cantidad de cada género en la comuna
        for resultado in resultados:
            if resultado[0] == comuna:
                generos[resultado[1]] += resultado[2]
                total_personas += resultado[2]

        # Configurar el gráfico circular
        fig, ax = plt.subplots()
        wedges, texts, autotexts = ax.pie(generos.values(), labels=generos.keys(), autopct=lambda pct: f"{pct:.1f}%\n{int(total_personas * pct / 100)} personas", startangle=90)
        ax.axis('equal')  # Asegura que el gráfico sea un círculo en lugar de una elipse
        ax.set_title(f"Comuna: {comuna}")  # Agregamos el título con el nombre de la comuna

        # Ajustar el tamaño de la fuente en los textos
        for text, autotext in zip(texts, autotexts):
            text.set(size=8)
            autotext.set(size=8)

        # Convertir la imagen a base64
        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        plt.close()
        imagen_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        imagenes_base64.append(imagen_base64)

    return imagenes_base64

def generar_grafico_respuestas():
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id_opc_respuesta_id, COUNT(*) FROM botApp_usuariorespuesta GROUP BY id_opc_respuesta_id"
        )
        resultados = cursor.fetchall()

    labels = []
    sizes = []

    for resultado in resultados:
        id_opc_respuesta, cantidad = resultado
        opcion_respuesta = PreguntaOpcionRespuesta.objects.get(id=id_opc_respuesta)
        labels.append(opcion_respuesta.OPC_Respuesta)
        sizes.append(cantidad)

    # Configurar el gráfico circular
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['lightgreen', 'lightcoral'])
    ax.axis('equal')  # Equal aspect ratio asegura que el gráfico sea circular.

    # Mostrar el gráfico
    plt.title('Respuestas a la pregunta')
    
    # Guardar la imagen en un buffer
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()

    # Convertir la imagen a base64
    imagen_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return imagen_base64

@login_required
def reportes(request):
    data = {
        "imagen_base64_ingresos": generar_grafico_respuestas_por_dia(),
        "imagen_base64_genero":  generar_grafico_personas_por_genero(),
        "imagen_base64_genero_comuna": generar_graficos_genero_por_comuna(),
        "imagen_base64_respuestas": generar_grafico_respuestas(),
            }
    return render(request, "reportes.html", data)


# --------------------- Formulario WEB --------------------- #
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
    
#TextoPreguntaUsuario
class UsuarioTextoPreguntaViewSet(viewsets.ModelViewSet):
    queryset = UsuarioTextoPregunta.objects.all()
    serializer_class = UsuarioTextoPreguntaSerializer
    


# --------------------- Api --------------------- #