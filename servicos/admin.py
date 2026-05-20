from django.contrib import admin

from .models import Servico
from candidaturas.models import Candidatura

class CandidaturaInline(admin.TabularInline):
    model = Candidatura
    extra = 1
    fields = ('freelancer', 'status')
    readonly_fields = ('freelancer',)

@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'empresa', 'data_hora', 'valor_hora')
    search_fields = ('nome', 'descricao', 'empresa__user__username', 'empresa__user__email')
    list_filter = ('data_hora',)
    inlines = [CandidaturaInline]
