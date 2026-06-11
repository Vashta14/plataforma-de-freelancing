from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.urls import reverse

from .models import Candidatura


@login_required(login_url='login')
def candidaturas(request):
    try:
        perfil = request.user.perfil
    except Exception:
        return HttpResponseForbidden('Acesso negado.')

    if perfil.tipo != 'empresa':
        return HttpResponseForbidden('Apenas empresas podem ver candidaturas.')

    candidaturas = Candidatura.objects.select_related('vaga', 'freelancer').filter(vaga__empresa=perfil).order_by('-vaga__data_hora')

    return render(request, 'candidaturas/lista_candidaturas.html', {'candidaturas': candidaturas})


@login_required(login_url='login')
def aceitar_candidatura(request, candidatura_id):
    if request.method != 'POST':
        return HttpResponseForbidden('Método não permitido.')

    candidatura = get_object_or_404(Candidatura, id=candidatura_id)
    try:
        perfil = request.user.perfil
    except Exception:
        return HttpResponseForbidden('Acesso negado.')

    if perfil.tipo != 'empresa' or candidatura.vaga.empresa != perfil:
        return HttpResponseForbidden('Você não pode aceitar esta candidatura.')

    if candidatura.vaga.status == 'cancelada':
        return HttpResponseForbidden('Não é possível aceitar candidaturas de serviços cancelados.')
    if candidatura.status != 'pendente':
        return HttpResponseForbidden('Esta candidatura já foi processada.')

    candidatura.status = 'aceita'
    candidatura.save(update_fields=['status'])
    url = reverse('detalhe_servico', args=[candidatura.vaga.id])
    return redirect(f"{url}?accepted_id={candidatura.id}")


@login_required(login_url='login')
def rejeitar_candidatura(request, candidatura_id):
    if request.method != 'POST':
        return HttpResponseForbidden('Método não permitido.')

    candidatura = get_object_or_404(Candidatura, id=candidatura_id)
    try:
        perfil = request.user.perfil
    except Exception:
        return HttpResponseForbidden('Acesso negado.')

    if perfil.tipo != 'empresa' or candidatura.vaga.empresa != perfil:
        return HttpResponseForbidden('Você não pode rejeitar esta candidatura.')

    if candidatura.vaga.status == 'cancelada':
        return HttpResponseForbidden('Não é possível rejeitar candidaturas de serviços cancelados.')
    if candidatura.status != 'pendente':
        return HttpResponseForbidden('Esta candidatura já foi processada.')

    candidatura.status = 'rejeitada'
    candidatura.save(update_fields=['status'])
    return redirect('detalhe_servico', candidatura.vaga.id)
