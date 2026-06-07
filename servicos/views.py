from django.shortcuts import render
from .models import Servico

def lista_de_servicos(request):
    servicos = Servico.objects.all()  
    return render(request, 'lista_de_itens.html', {'itens': servicos, 'titulo': 'Lista de Serviços'})