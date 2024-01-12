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
    Datos = Usuario.objects.all()
    data = {
        'form': UsuarioForm(),
        'Datos': Datos,
        'imagen_base64_ingresos': generar_grafico_lineas_ingresos(),
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

    return render(request, 'home.html', data)


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