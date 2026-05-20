import uuid

from django.db import models


class Habilidade(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    descricao = models.CharField(max_length=255)

    def __str__(self):
        return self.descricao


class HabilidadeUsuario(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(
        'perfis.Perfil',
        on_delete=models.CASCADE,
        related_name='habilidades_usuario',
    )
    habilidade = models.ForeignKey(
        Habilidade,
        on_delete=models.CASCADE,
        related_name='perfis_habilidade',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['usuario', 'habilidade'], name='unique_usuario_habilidade')
        ]
