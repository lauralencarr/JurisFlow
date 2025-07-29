from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Evento
from .models import Cliente

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # redireciona após login
        else:
            messages.error(request, 'Usuário ou senha inválidos.')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


def cadastro_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'As senhas não coincidem.')
            return render(request, 'cadastro.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Usuário já existe.')
            return render(request, 'cadastro.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('home')

    return render(request, 'cadastro.html')

def processos_view(request):
    return render (request, 'processos.html')

def calendario_view(request):
    return render(request, 'calendario.html')

def home_view(request):
    hoje = timezone.now().date()
    eventos_hoje = Evento.objects.filter(data__date=hoje).order_by('hora')

    return render(request, 'home.html', {
        'eventos_hoje': eventos_hoje
    })

def financas_view(request):
    clientes = Cliente.objects.all()
    return render(request, 'financas.html', {
        'clientes': clientes
    })

    
def eventos_view(request):
    clientes = Cliente.objects.all().values_list('nome')
    tipo_choices = Evento.TIPO_CHOICES

    if request.method == 'POST':
        # Aqui você trataria o formulário depois
        pass

    return render(request, 'eventos.html', { 
        'tipo_choices': tipo_choices,
        'clientes': clientes,
    })

def criar_processo(request):
    if request.method == 'POST':
        form = ProcessoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_processos')  # ou onde quiser redirecionar
    else:
        form = ProcessoForm()
    return render(request, 'processos/criar_processo.html', {'form': form})