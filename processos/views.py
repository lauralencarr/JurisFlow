import json
import calendar
from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Sum, Count
from django.http import JsonResponse

from .models import Evento, Cliente, Processo, TransacaoFinanceira
from .forms import ClienteForm, ProcessoForm, EventoForm, TransacaoForm

MONTH_ABBR_PT = {
    1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr',
    5: 'Mai', 6: 'Jun', 7: 'Jul', 8: 'Ago',
    9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez',
}

COLOR_EVENTO = {
    'audiencia': '#DC2626',
    'reuniao': '#2563EB',
    'prazo': '#D97706',
    'documento': '#7C3AED',
    'consultoria': '#059669',
    'outro': '#64748B',
}


# ── Auth ──────────────────────────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def cadastro_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm = request.POST.get('confirm_password', '')
        if password != confirm:
            messages.error(request, 'As senhas não coincidem.')
            return render(request, 'cadastro.html')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Esse usuário já existe.')
            return render(request, 'cadastro.html')
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'cadastro.html')


# ── Dashboard ─────────────────────────────────────────────────────────────────

@login_required
def home_view(request):
    hoje = timezone.now().date()
    eventos_hoje = Evento.objects.filter(data__date=hoje).select_related(
        'processo', 'processo__cliente'
    ).order_by('data')
    processos_recentes = Processo.objects.select_related('cliente').order_by('-data_abertura')[:5]

    total_processos = Processo.objects.count()
    total_clientes = Cliente.objects.count()
    processos_ativos = Processo.objects.filter(status='aberto').count()
    receita_total = (
        TransacaoFinanceira.objects.filter(situacao='pago')
        .aggregate(total=Sum('valor'))['total'] or 0
    )

    return render(request, 'home.html', {
        'eventos_hoje': eventos_hoje,
        'processos_recentes': processos_recentes,
        'total_processos': total_processos,
        'total_clientes': total_clientes,
        'processos_ativos': processos_ativos,
        'receita_total': receita_total,
        'page': 'home',
    })


# ── Processos ─────────────────────────────────────────────────────────────────

@login_required
def processos_view(request):
    form = ProcessoForm()
    if request.method == 'POST':
        form = ProcessoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Processo cadastrado com sucesso.')
            return redirect('processos')

    processos = Processo.objects.select_related('cliente').order_by('-data_abertura')
    return render(request, 'processos.html', {
        'form': form,
        'processos': processos,
        'page': 'processos',
    })


@login_required
def processo_delete_view(request, pk):
    processo = get_object_or_404(Processo, pk=pk)
    if request.method == 'POST':
        processo.delete()
        messages.success(request, 'Processo removido com sucesso.')
    return redirect('processos')


# ── Clientes ──────────────────────────────────────────────────────────────────

@login_required
def clientes_view(request):
    form = ClienteForm()
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente cadastrado com sucesso.')
            return redirect('clientes')

    clientes = Cliente.objects.annotate(num_processos=Count('processos')).order_by('nome')
    return render(request, 'clientes.html', {
        'form': form,
        'clientes': clientes,
        'page': 'clientes',
    })


@login_required
def cliente_delete_view(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente removido com sucesso.')
    return redirect('clientes')


# ── Calendário ────────────────────────────────────────────────────────────────

@login_required
def calendario_view(request):
    return render(request, 'calendario.html', {'page': 'calendario'})


@login_required
def eventos_api_view(request):
    eventos = Evento.objects.select_related('processo', 'processo__cliente').all()
    data = [
        {
            'id': e.pk,
            'title': f"{e.get_tipo_display()} — {e.processo.cliente.nome}",
            'start': e.data.isoformat(),
            'color': COLOR_EVENTO.get(e.tipo, '#64748B'),
            'extendedProps': {
                'tipo': e.get_tipo_display(),
                'local': e.local or '',
                'descricao': e.descricao or '',
                'processo': str(e.processo),
            },
        }
        for e in eventos
    ]
    return JsonResponse(data, safe=False)


# ── Eventos ───────────────────────────────────────────────────────────────────

@login_required
def evento_criar_view(request):
    form = EventoForm()
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Evento criado com sucesso.')
            return redirect('calendario')

    return render(request, 'eventos.html', {
        'form': form,
        'page': 'calendario',
    })


@login_required
def evento_delete_view(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    if request.method == 'POST':
        evento.delete()
        messages.success(request, 'Evento removido com sucesso.')
    return redirect('calendario')


# ── Finanças ──────────────────────────────────────────────────────────────────

@login_required
def financas_view(request):
    receita_total = (
        TransacaoFinanceira.objects.filter(situacao='pago')
        .aggregate(total=Sum('valor'))['total'] or 0
    )
    pendente_total = (
        TransacaoFinanceira.objects.filter(situacao='pendente')
        .aggregate(total=Sum('valor'))['total'] or 0
    )
    transacoes = TransacaoFinanceira.objects.select_related(
        'processo', 'processo__cliente'
    ).order_by('-data')

    hoje = date.today()
    dados_mensais = []
    for i in range(5, -1, -1):
        m = hoje.month - i
        y = hoje.year
        while m <= 0:
            m += 12
            y -= 1
        total = (
            TransacaoFinanceira.objects.filter(situacao='pago', data__year=y, data__month=m)
            .aggregate(total=Sum('valor'))['total'] or 0
        )
        dados_mensais.append({'mes': f"{MONTH_ABBR_PT[m]}/{str(y)[2:]}", 'total': float(total)})

    form = TransacaoForm()
    if request.method == 'POST':
        form = TransacaoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transação registrada com sucesso.')
            return redirect('financas')

    return render(request, 'financas.html', {
        'receita_total': receita_total,
        'pendente_total': pendente_total,
        'transacoes': transacoes,
        'dados_mensais': json.dumps(dados_mensais),
        'form': form,
        'page': 'financas',
    })
