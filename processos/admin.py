from django.contrib import admin
from .models import Cliente, Processo, Evento, TransacaoFinanceira


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone')
    search_fields = ('nome', 'email')


@admin.register(Processo)
class ProcessoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'cliente', 'tipo', 'valor', 'status', 'data_abertura')
    list_filter = ('status', 'tipo')
    search_fields = ('numero', 'cliente__nome')


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'processo', 'data', 'local')
    list_filter = ('tipo',)
    search_fields = ('titulo', 'processo__numero', 'processo__cliente__nome')


@admin.register(TransacaoFinanceira)
class TransacaoFinanceiraAdmin(admin.ModelAdmin):
    list_display = ('processo', 'valor', 'situacao', 'data')
    list_filter = ('situacao',)
    search_fields = ('processo__numero', 'processo__cliente__nome')
