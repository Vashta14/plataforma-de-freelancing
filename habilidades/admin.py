from django.contrib import admin

from .models import Habilidade, HabilidadeUsuario


@admin.register(Habilidade)
class HabilidadeAdmin(admin.ModelAdmin):
    list_display = ('descricao',)
    search_fields = ('descricao',)


@admin.register(HabilidadeUsuario)
class HabilidadeUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'habilidade')
    search_fields = ('usuario__user__username', 'usuario__user__email', 'habilidade__descricao')
    list_filter = ('habilidade',)
