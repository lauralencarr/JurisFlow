from django import forms
from .models import Cliente, Processo, Evento, TransacaoFinanceira


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'email', 'telefone']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@exemplo.com'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(11) 99999-9999'}),
        }
        labels = {
            'nome': 'Nome',
            'email': 'E-mail',
            'telefone': 'Telefone',
        }


class ProcessoForm(forms.ModelForm):
    class Meta:
        model = Processo
        fields = ['numero', 'cliente', 'tipo', 'descricao', 'valor', 'status']
        widgets = {
            'numero': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 0001.234.5678/2024'}),
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descrição do processo...'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0,00'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'numero': 'Número do Processo',
            'cliente': 'Cliente',
            'tipo': 'Tipo',
            'descricao': 'Descrição',
            'valor': 'Valor (R$)',
            'status': 'Status',
        }


class EventoForm(forms.ModelForm):
    data = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],
        label='Data e Horário',
    )

    class Meta:
        model = Evento
        fields = ['tipo', 'processo', 'data', 'local', 'descricao']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'processo': forms.Select(attrs={'class': 'form-select'}),
            'local': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Local do evento'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Detalhes do evento...'}),
        }
        labels = {
            'tipo': 'Tipo de Evento',
            'processo': 'Processo',
            'local': 'Local',
            'descricao': 'Descrição',
        }


class TransacaoForm(forms.ModelForm):
    class Meta:
        model = TransacaoFinanceira
        fields = ['processo', 'valor', 'situacao']
        widgets = {
            'processo': forms.Select(attrs={'class': 'form-select'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0,00'}),
            'situacao': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'processo': 'Processo',
            'valor': 'Valor (R$)',
            'situacao': 'Situação',
        }
