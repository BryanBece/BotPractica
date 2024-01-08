from .forms import RespuestaForm
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
        cursor.execute('SELECT COUNT(*), fecha_ingreso FROM botApp_respuesta GROUP BY fecha_ingreso')
        resultados = cursor.fetchall()

    categorias = [str(result[1].strftime('%d/%m/%Y')) for result in resultados]
    valores = [result[0] for result in resultados]

    plt.plot(categorias, valores, marker='o', linestyle='-', color='blue')
    plt.xlabel('Fechas de Ingreso')
    plt.ylabel('Número de Registros')
    plt.title('Gráfico de Líneas')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    imagen_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return imagen_base64


def generar_grafico_lineas_genero():
    with connection.cursor() as cursor:
        cursor.execute('SELECT genero_id, COUNT(*) FROM botApp_respuesta GROUP BY genero_id')
        resultados = cursor.fetchall()

    generos = [Genero.objects.get(id=result[0]).nombre for result in resultados]
    cantidades = [result[1] for result in resultados]

    plt.plot(generos, cantidades, marker='o', linestyle='-', color='green')
    plt.xlabel('Género')
    plt.ylabel('Número de Registros')
    plt.title('Gráfico de Líneas por Género')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    imagen_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return imagen_base64


def generar_grafico_lineas_ingresos_por_mes():
    with connection.cursor() as cursor:
        cursor.execute('SELECT DATE_FORMAT(fecha_ingreso, "%Y-%m") AS mes, COUNT(*) FROM botApp_respuesta GROUP BY mes ORDER BY mes')
        resultados = cursor.fetchall()

    meses = [result[0] for result in resultados]
    cantidades = [result[1] for result in resultados]

    plt.plot(meses, cantidades, marker='o', linestyle='-', color='purple')
    plt.xlabel('Mes')
    plt.ylabel('Número de Ingresos')
    plt.title('Ingresos por Mes')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    imagen_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return imagen_base64


@login_required
def home(request):
    Datos = Respuesta.objects.all()
    data = {
        'form': RespuestaForm(),
        'Datos': Datos,
        'imagen_base64_ingresos': generar_grafico_lineas_ingresos(),
        'imagen_base64_genero': generar_grafico_lineas_genero(),
        'imagen_base64_ingresos_por_mes': generar_grafico_lineas_ingresos_por_mes(),
    }

    if request.method == 'POST':
        form = RespuestaForm(request.POST)

        if form.is_valid():
            form.instance.id_usuario = request.user.id
            form.save()
            messages.success(request, 'Datos guardados correctamente')
            form = RespuestaForm()
        else:
            print(form.errors)
            messages.error(request, 'La persona debe tener más de 18 años y haber nacido después de 1930.')
            form = RespuestaForm()

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