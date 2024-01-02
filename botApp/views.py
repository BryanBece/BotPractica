from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.shortcuts import render, redirect
from django.contrib import messages


# Create your views here.

@login_required(login_url='/login/') 
def home(request):
    Datos = Formulario.objects.all()
    data = {
        'form': FormularioForm(),
        'Datos': Datos
    }

    if request.method == 'POST':
        anioNacimiento = request.POST.get('anioNacimiento')
        comuna = request.POST.get('comuna')
        genero = request.POST.get('genero')
        
        form = Formulario(anioNacimiento=anioNacimiento, comuna=comuna, genero=genero)
        form.save()
        
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
            return render(request, 'login.html') 

    return render(request, 'login.html')