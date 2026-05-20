from django.contrib import admin

from .models import Avaliacao


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('servico', 'usuario', 'tipo', 'nota', 'criado_em')
    search_fields = ('servico__nome', 'usuario__user__username', 'usuario__user__email', 'comentario')
    list_filter = ('nota', 'tipo', 'criado_em')
