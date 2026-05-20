from django.contrib import admin

from .models import Perfil

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'tipo', 'telefone')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'telefone')
    list_filter = ('tipo',)

