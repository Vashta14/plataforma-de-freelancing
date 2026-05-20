from django.contrib import admin

from .models import Servico
from candidaturas.models import Candidatura
from avaliacoes.models import Avaliacao


class CandidaturaInline(admin.TabularInline):
    model = Candidatura
    extra = 1
    fields = ('freelancer', 'status')
    readonly_fields = ('freelancer',)
    
class AvalicaoInline(admin.TabularInline):
    model = Avaliacao
    extra = 1
    fields = ('usuario', 'nota',  'tipo', 'comentario', 'criado_em')
    readonly_fields = ('usuario', 'nota',  'tipo', 'comentario', 'criado_em')


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'empresa', 'data_hora', 'valor_hora')
    search_fields = ('nome', 'descricao', 'empresa__user__username', 'empresa__user__email')
    list_filter = ('data_hora',)
    inlines = [CandidaturaInline, AvalicaoInline]
