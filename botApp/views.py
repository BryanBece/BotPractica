from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.db import connection
import matplotlib.pyplot as plt
from io import BytesIO
import base64


# Create your views here.

def generar_grafico_lineas_ingresos():
    # Consulta para obtener el conteo de registros y las fechas de ingreso
    with connection.cursor() as cursor:
        cursor.execute('SELECT COUNT(*), fecha_ingreso FROM botApp_formulario GROUP BY fecha_ingreso')
        resultados = cursor.fetchall()

    # Separar los resultados en las listas de eje X y eje Y
    categorias = [str(result[1].strftime('%d/%m/%Y')) for result in resultados]
    valores = [result[0] for result in resultados]

    # Crear el gráfico de líneas
    plt.plot(categorias, valores, marker='o', linestyle='-', color='blue')
    plt.xlabel('Fechas de Ingreso')
    plt.ylabel('Número de Registros')
    plt.title('Gráfico de Líneas')

    # Convertir el gráfico a bytes
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Convertir a base64 para incrustar en la plantilla HTML
    imagen_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return imagen_base64


def generar_grafico_lineas_genero():
    # Consulta para obtener el conteo de registros por género
    with connection.cursor() as cursor:
        cursor.execute('SELECT genero, COUNT(*) FROM botApp_formulario GROUP BY genero')
        resultados = cursor.fetchall()

    # Separar los resultados en las listas de eje X y eje Y
    generos = [result[0] for result in resultados]
    cantidades = [result[1] for result in resultados]

    # Crear el gráfico de líneas
    plt.plot(generos, cantidades, marker='o', linestyle='-', color='green')
    plt.xlabel('Género')
    plt.ylabel('Número de Registros')
    plt.title('Gráfico de Líneas por Género')

    # Convertir el gráfico a bytes
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Convertir a base64 para incrustar en la plantilla HTML
    imagen_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return imagen_base64

def generar_grafico_lineas_ingresos_por_mes():
    # Consulta para obtener el conteo de registros por mes
    with connection.cursor() as cursor:
        cursor.execute('SELECT strftime(\'%Y-%m\', fecha_ingreso) AS mes, COUNT(*) FROM botApp_formulario GROUP BY mes ORDER BY mes')
        resultados = cursor.fetchall()

    # Separar los resultados en las listas de eje X y eje Y
    meses = [result[0] for result in resultados]
    cantidades = [result[1] for result in resultados]

    # Crear el gráfico de líneas
    plt.plot(meses, cantidades, marker='o', linestyle='-', color='purple')
    plt.xlabel('Mes')
    plt.ylabel('Número de Ingresos')
    plt.title('Ingresos por Mes')

    # Convertir el gráfico a bytes
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Convertir a base64 para incrustar en la plantilla HTML
    imagen_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return imagen_base64



@login_required
def home(request):
    Datos = Formulario.objects.all()
    data = {
        'form': FormularioForm(),
        'Datos': Datos,
        'imagen_base64_ingresos': generar_grafico_lineas_ingresos(),
        'imagen_base64_genero': generar_grafico_lineas_genero(),
        'imagen_base64_ingresos_por_mes': generar_grafico_lineas_ingresos_por_mes(),
    
    }

    if request.method == 'POST':
        form = FormularioForm(request.POST)

        if form.is_valid():
            form.instance.usuario = request.user.username
            form.save()
            messages.success(request, 'Datos guardados correctamente')
            form = FormularioForm()  
        else:
            messages.error(request, 'La persona debe tener más de 18 años y haber nacido después de 1930.')
            form = FormularioForm()  

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



