import uuid

from django.contrib.auth.models import User
from django.db import models


class Perfil(models.Model):
    TIPOS_PERFIL = (
        ('empresa', 'Empresa'),
        ('freelancer', 'Freelancer'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    descricao = models.TextField(blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    tipo = models.CharField(max_length=20, choices=TIPOS_PERFIL)

    def __str__(self):
        nome_completo = self.user.get_full_name().strip()
        return nome_completo or self.user.username
