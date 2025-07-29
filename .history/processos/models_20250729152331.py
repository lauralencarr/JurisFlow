from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)

    def __str__(self):
        return self.nome

class Processo(models.Model):
    numero = models.CharField(max_length=50, unique=True)
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE, related_name='processos')
    descricao = models.TextField()
    data_abertura = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, default='aberto')

    def __str__(self):
        return f"{self.numero} - {self.cliente.nome}"
    
class Evento(models.Model):
    TIPO_CHOICES = [
        ('reuniao', 'Reunião com cliente'),
        ('audiencia', 'Audiência'),
        ('prazo', 'Prazo Processual'),
        ('documento', 'Envio de Documentação'),
        ('consultoria', 'Consultoria Jurídica'),
        ('outro', 'Outro')
    ]

    titulo = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100, choices=TIPO_CHOICES)
    data = models.DateTimeField()
    local = models.CharField(max_length=100, blank=True, null=True)
    processo = models.ForeignKey(Processo, on_delete=models.CASCADE, related_name='atividades')
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.processo.cliente.nome} ({self.data.strftime('%d/%m/%Y')})"


class TransacaoFinanceira(models.Model):
    processo = models.ForeignKey(Processo, on_delete=models.CASCADE, related_name='transacoes')
    data = models.DateField(auto_now_add=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    situacao = models.CharField(max_length=20, choices=[
        ('pago', 'Pago'),
        ('pendente', 'Pendente'),
        ('cancelado', 'Cancelado'),
        ('reembolsado', 'Reembolsado'),
    ])

    def __str__(self):
        return f"{self.processo.numero} - {self.processo.cliente.nome} - R${self.valor} ({self.situacao})"

