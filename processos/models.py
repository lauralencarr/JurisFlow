from django.db import models


class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)

    def __str__(self):
        return self.nome


class Processo(models.Model):
    TIPO_CHOICES = [
        ('civil', 'Cível'),
        ('criminal', 'Criminal'),
        ('trabalhista', 'Trabalhista'),
        ('familia', 'Família'),
        ('constitucional', 'Constitucional'),
        ('tributario', 'Tributário'),
        ('outro', 'Outro'),
    ]
    STATUS_CHOICES = [
        ('aberto', 'Aberto'),
        ('encerrado', 'Encerrado'),
        ('arquivado', 'Arquivado'),
        ('suspenso', 'Suspenso'),
    ]

    numero = models.CharField(max_length=50, unique=True)
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE, related_name='processos')
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES, default='civil')
    descricao = models.TextField()
    valor = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    data_abertura = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aberto')

    def __str__(self):
        return f"{self.numero} - {self.cliente.nome}"


class Evento(models.Model):
    TIPO_CHOICES = [
        ('reuniao', 'Reunião com cliente'),
        ('audiencia', 'Audiência'),
        ('prazo', 'Prazo Processual'),
        ('documento', 'Envio de Documentação'),
        ('consultoria', 'Consultoria Jurídica'),
        ('outro', 'Outro'),
    ]

    titulo = models.CharField(max_length=100, blank=True, default='')
    tipo = models.CharField(max_length=100, choices=TIPO_CHOICES)
    data = models.DateTimeField()
    local = models.CharField(max_length=100, blank=True, null=True)
    processo = models.ForeignKey(Processo, on_delete=models.CASCADE, related_name='atividades')
    descricao = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['data']

    def save(self, *args, **kwargs):
        if not self.titulo:
            self.titulo = self.get_tipo_display()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.processo.cliente.nome} ({self.data.strftime('%d/%m/%Y')})"


class TransacaoFinanceira(models.Model):
    SITUACAO_CHOICES = [
        ('pago', 'Pago'),
        ('pendente', 'Pendente'),
        ('cancelado', 'Cancelado'),
        ('reembolsado', 'Reembolsado'),
    ]

    processo = models.ForeignKey(Processo, on_delete=models.CASCADE, related_name='transacoes')
    data = models.DateField(auto_now_add=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    situacao = models.CharField(max_length=20, choices=SITUACAO_CHOICES)

    def __str__(self):
        return f"{self.processo.numero} - R${self.valor} ({self.situacao})"
