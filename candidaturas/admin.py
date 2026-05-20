from django.contrib import admin

from .models import Candidatura


@admin.register(Candidatura)
class CandidaturaAdmin(admin.ModelAdmin):
    list_display = ('vaga', 'freelancer', 'status')
    search_fields = ('vaga__nome', 'freelancer__user__username', 'freelancer__user__email')
    list_filter = ('status',)
    autocomplete_fields = ('vaga', 'freelancer',)
