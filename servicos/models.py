import uuid

from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Servico(models.Model):
    STATUS_CHOICES = (
        ('aberta', 'Aberta'),
        ('fechada', 'Fechada'),
        ('cancelada', 'Cancelada'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    empresa = models.ForeignKey(
        'perfis.Perfil',
        on_delete=models.CASCADE,
        related_name='vagas',
    )
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    data_hora = models.DateTimeField()
    valor_hora = models.DecimalField(max_digits=10, decimal_places=2)
    duracao = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aberta')
    
    def clean(self):
        if self.data_hora and self.data_hora < timezone.now():
            raise ValidationError('A data e hora devem ser futuras.')

    def __str__(self):
        return self.nome

