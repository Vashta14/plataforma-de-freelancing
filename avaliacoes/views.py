from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .forms import AvaliacaoForm
from .models import Avaliacao
from servicos.models import Servico
from perfis.models import Perfil
from candidaturas.models import Candidatura


@login_required(login_url='login')
def avaliar_freelancer(request, servico_id, perfil_id):
    servico = get_object_or_404(Servico, id=servico_id)
    freelancer = get_object_or_404(Perfil, id=perfil_id)

    try:
        perfil = request.user.perfil
    except Exception:
        return HttpResponseForbidden('Acesso negado.')

    if perfil.tipo != 'empresa' or servico.empresa != perfil:
        return HttpResponseForbidden('Apenas a empresa dona do serviço pode avaliar.')

    if not Candidatura.objects.filter(vaga=servico, freelancer=freelancer, status='aceita').exists():
        return HttpResponseForbidden('Avaliação permitida apenas para freelancers com candidatura aceita.')

    if Avaliacao.objects.filter(servico=servico, usuario=freelancer, tipo='freelancer').exists():
        return render(request, 'avaliacoes/avaliar_freelancer.html', {
            'form': AvaliacaoForm(),
            'servico': servico,
            'freelancer': freelancer,
            'nota_choices': range(1, 6),
            'already_evaluated': True,
        })

    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            aval = form.save(commit=False)
            aval.servico = servico
            aval.usuario = freelancer
            aval.tipo = 'freelancer'
            aval.save()
            return redirect('detalhe_servico', servico.id)
    else:
        form = AvaliacaoForm()

    return render(request, 'avaliacoes/avaliar_freelancer.html', {
        'form': form,
        'servico': servico,
        'freelancer': freelancer,
        'nota_choices': range(1, 6),
        'already_evaluated': False,
    })


@login_required(login_url='login')
def avaliar_empresa(request, servico_id):
    servico = get_object_or_404(Servico.objects.select_related('empresa__user'), id=servico_id)

    try:
        perfil = request.user.perfil
    except Exception:
        return HttpResponseForbidden('Acesso negado.')

    if perfil.tipo != 'freelancer':
        return HttpResponseForbidden('Apenas freelancers podem avaliar empresas.')

    candidatura_aceita = Candidatura.objects.filter(
        vaga=servico,
        freelancer=perfil,
        status='aceita',
    ).exists()
    if not candidatura_aceita or servico.status != 'finalizado':
        return HttpResponseForbidden(
            'A empresa só pode ser avaliada após a candidatura ser aceita e o serviço finalizado.'
        )

    if Avaliacao.objects.filter(
        servico=servico,
        usuario=servico.empresa,
        tipo='servico',
    ).exists():
        return render(request, 'avaliacoes/avaliar_empresa.html', {
            'form': AvaliacaoForm(),
            'servico': servico,
            'nota_choices': range(1, 6),
            'already_evaluated': True,
        })

    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.servico = servico
            avaliacao.usuario = servico.empresa
            avaliacao.tipo = 'servico'
            avaliacao.save()
            return redirect('detalhe_servico_freelancer', servico.id)
    else:
        form = AvaliacaoForm()

    return render(request, 'avaliacoes/avaliar_empresa.html', {
        'form': form,
        'servico': servico,
        'nota_choices': range(1, 6),
        'already_evaluated': False,
    })
