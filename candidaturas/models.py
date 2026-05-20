import uuid

from django.db import models


class Candidatura(models.Model):
    STATUS_CHOICES = (
        ('aceita', 'Aceita'),
        ('pendente', 'Pendente'),
         ('rejeitada', 'Rejeitada'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vaga = models.ForeignKey(
        'servicos.Servico',
        on_delete=models.CASCADE,
        related_name='candidaturas',
    )
    freelancer = models.ForeignKey(
        'perfis.Perfil',
        on_delete=models.CASCADE,
        related_name='candidaturas',
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['vaga', 'freelancer'], name='unique_vaga_freelancer')
        ]
    def __str__(self):
        return f'Candidatura de {self.freelancer} para {self.vaga}'
