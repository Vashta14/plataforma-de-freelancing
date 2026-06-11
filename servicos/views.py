from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError

from .models import Servico
from candidaturas.models import Candidatura
from .forms import CriarServicoForm


def lista_de_servicos(request):
    if request.user.is_authenticated:
        try:
            if request.user.perfil.tipo == 'freelancer':
                return redirect('encontrar_servicos')
        except Exception:
            pass
    servicos = Servico.objects.select_related('empresa').all()
    return render(request, 'servicos/lista_de_itens.html', {'servicos': servicos})


@login_required(login_url='login')
def criar_servico(request):
    try:
        perfil = request.user.perfil
    except Exception:
        return HttpResponseForbidden('Acesso negado.')

    if perfil.tipo != 'empresa':
        return HttpResponseForbidden('Apenas empresas podem criar serviços.')

    if request.method == 'POST':
        form = CriarServicoForm(request.POST)
        if form.is_valid():
            servico = form.save(commit=False)
            servico.empresa = perfil
            servico.status = 'aberta'

            try:
                servico.full_clean()
                servico.save()
                return redirect('detalhe_servico', servico.id)
            except ValidationError as e:
                form.add_error(None, str(e))
    else:
        form = CriarServicoForm()

    return render(request, 'servicos/criar_servico.html', {'form': form})


@login_required(login_url='login')
def editar_servico(request, servico_id):
    servico = get_object_or_404(Servico, id=servico_id)

    try:
        perfil = request.user.perfil
    except Exception:
        return HttpResponseForbidden('Acesso negado.')

    if servico.empresa != perfil:
        return HttpResponseForbidden('Você não tem permissão para editar este serviço.')

    if request.method == 'POST':
        form = CriarServicoForm(request.POST, instance=servico)
        if form.is_valid():
            servico = form.save(commit=False)
            servico.empresa = perfil
            try:
                servico.full_clean()
                servico.save()
                return redirect('detalhe_servico', servico.id)
            except ValidationError as e:
                form.add_error(None, str(e))
    else:
        form = CriarServicoForm(instance=servico)

    return render(request, 'servicos/editar_servico.html', {'form': form, 'servico': servico})


@login_required(login_url='login')
def detalhe_servico(request, servico_id):
    servico = get_object_or_404(Servico, id=servico_id)

    perfil = None
    if request.user.is_authenticated:
        try:
            perfil = request.user.perfil
        except Exception:
            perfil = None

    if perfil and perfil.tipo == 'empresa' and servico.empresa != perfil:
        return HttpResponseForbidden('Você não tem permissão para ver este serviço.')
    if perfil and perfil.tipo == 'freelancer':
        return redirect('detalhe_servico_freelancer', servico.id)

    candidaturas = None
    is_empresa_owner = False
    accepted_modal = None
    accepted_exists = False
    if perfil and perfil.tipo == 'empresa' and servico.empresa == perfil:
        is_empresa_owner = True
        candidaturas = Candidatura.objects.select_related('freelancer__user').filter(vaga=servico).order_by('-id')
        accepted_exists = candidaturas.filter(status='aceita').exists()

        accepted_id = request.GET.get('accepted_id')
        if accepted_id:
            try:
                accepted_candidate = candidaturas.get(id=accepted_id, status='aceita')
                phone = ''.join(ch for ch in (accepted_candidate.freelancer.telefone or '') if ch.isdigit())
                accepted_modal = {
                    'freelancer_name': accepted_candidate.freelancer.user.get_full_name() or accepted_candidate.freelancer.user.username,
                    'whatsapp_url': f'https://wa.me/{phone}' if phone else '',
                }
            except Candidatura.DoesNotExist:
                accepted_modal = None

    return render(request, 'servicos/detalhe_servico.html', {
        'servico': servico,
        'candidaturas': candidaturas,
        'is_empresa_owner': is_empresa_owner,
        'accepted_exists': accepted_exists,
        'accepted_modal': accepted_modal,
    })


@login_required(login_url='login')
@require_POST
def cancelar_servico(request, servico_id):
    servico = get_object_or_404(Servico, id=servico_id)

    try:
        perfil = request.user.perfil
    except Exception:
        return HttpResponseForbidden('Acesso negado.')

    if servico.empresa != perfil:
        return HttpResponseForbidden('Você não tem permissão para cancelar este serviço.')

    if servico.status == 'finalizado':
        return HttpResponseForbidden('Serviços finalizados não podem ser cancelados.')

    servico.status = 'cancelada'
    if servico.status == 'finalizado':
        return HttpResponseForbidden('Serviços finalizados não podem ser cancelados.')

    servico.status = 'cancelada'

    return redirect('dashboard_empresa')


@login_required(login_url='login')
@require_POST
def finalizar_servico(request, servico_id):
    servico = get_object_or_404(Servico, id=servico_id)

    try:
        perfil = request.user.perfil
    except Exception:
        return HttpResponseForbidden('Acesso negado.')

    if servico.empresa != perfil:
        return HttpResponseForbidden('Você não tem permissão para finalizar este serviço.')

    if servico.status == 'cancelada' or servico.status == 'finalizado':
        return HttpResponseForbidden('Este serviço não pode ser finalizado.')

    if not Candidatura.objects.filter(vaga=servico, status='aceita').exists():
        return HttpResponseForbidden('Só é possível finalizar serviço após aceitar uma candidatura.')

    servico.status = 'finalizado'
    servico.save(update_fields=['status'])
    return redirect('detalhe_servico', servico.id)
