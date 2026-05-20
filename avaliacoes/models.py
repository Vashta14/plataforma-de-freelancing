import uuid

from django.db import models


class Avaliacao(models.Model):
    TIPO_CHOICES = (
        ('servico', 'Serviço'),
        ('freelancer', 'Freelancer'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    servico = models.ForeignKey(
        'servicos.Servico',
        on_delete=models.CASCADE,
        related_name='avaliacoes',
    )
    usuario = models.ForeignKey(
        'perfis.Perfil',
        on_delete=models.CASCADE,
        related_name='avaliacoes',
    )
    
    nota = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 11)]
    )
    comentario = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['servico', 'usuario', 'tipo'], name='unique_servico_usuario_tipo')
        ]

    def __str__(self):
        return f'Avaliação {self.tipo} nota {self.nota}'
    
    
