from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from django.shortcuts import render, redirect
from django.db import connection
import matplotlib.pyplot as plt
from io import BytesIO
import base64


def generar_grafico_lineas_ingresos():
    with connection.cursor() as cursor:
        cursor.execute('SELECT COUNT(*) FROM botApp_usuario')
        total_usuarios = cursor.fetchone()[0]

    categorias = ['Total Usuarios']
    valores = [total_usuarios]

    plt.plot(categorias, valores, marker='o', linestyle='-', color='blue')
    plt.xlabel('Categorías')
    plt.ylabel('Número de Usuarios')
    plt.title('Gráfico de Líneas')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    imagen_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return imagen_base64



@login_required
def home(request):
    return render(request, 'home.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')  
        else:
            return render(request, 'registration/login.html') 

    return render(request, 'registration/login.html')

#Base de datos
@login_required
def database(request):
    Datos = Usuario.objects.all()
    data = {
        'Datos': Datos,
    }
    return render(request, 'database.html', data)

#Reportes
@login_required
def reportes(request):
    data = {
        'imagen_base64_ingresos': generar_grafico_lineas_ingresos(),
    }
    return render(request, 'reportes.html', data)

#Formulario
@login_required
def formulario(request):
    data = {
        'form': UsuarioForm(),
    }

    if request.method == 'POST':
        form = UsuarioForm(request.POST)

        if form.is_valid():
            form.instance.id_usuario = request.user.id
            form.save()
            print(form.cleaned_data)
            messages.success(request, 'Datos guardados correctamente')
            form = UsuarioForm()
            
        else:
            print(form.errors)
            messages.error(request, 'La persona debe tener más de 18 años y haber nacido después de 1930.')
            form = UsuarioForm()

    return render(request, 'formulario.html', data)  

# --------------------- Preguntas --------------------- #
@login_required
def preguntasHome(request):
    return render(request, 'preguntas/preguntasHome.html')

#Listar Preguntas
@login_required
def listarPreguntas(request):
    Preguntas = Pregunta.objects.all()
    data = {
        'preguntas': Preguntas,
    }
    return render(request, 'preguntas/listarPreguntas.html', data)

#Modificar Pregunta
@login_required
def modificarPregunta(request, id):
    Preguntas = Pregunta.objects.get(id=id)
    data = {
        'form': PreguntaForm(instance=Preguntas)
    }

    if request.method == 'POST':
        formulario = PreguntaForm(data=request.POST, instance=Preguntas, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado Correctamente")
            return redirect(to="listarPreguntas")
        data["form"] = formulario

    return render(request, 'preguntas/modificarPreguntas.html', data)

#Eliminar Pregunta
@login_required
def eliminarPregunta(request, id):
    Preguntas = Pregunta.objects.get(id=id)
    Preguntas.delete()
    messages.success(request, "Eliminado Correctamente")
    return redirect(to="listarPreguntas")

#Crear Pregunta
@login_required
def crearPregunta(request):
    data = {
        'form': PreguntaForm()
    }

    if request.method == 'POST':
        formulario = PreguntaForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Pregunta Creada Correctamente")
        else:
            data["form"] = formulario

    return render(request, 'preguntas/crearPreguntas.html', data)