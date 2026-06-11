from datetime import datetime
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.db.models import Avg, Count, Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from avaliacoes.models import Avaliacao
from candidaturas.models import Candidatura
from habilidades.models import Habilidade, HabilidadeUsuario
from servicos.models import Servico

from .forms import ContaForm, PerfilForm
from .models import Perfil


def _perfil_freelancer(request):
    try:
        perfil = request.user.perfil
    except Perfil.DoesNotExist:
        return None
    return perfil if perfil.tipo == 'freelancer' else None


def _candidaturas_do_freelancer(perfil, status=''):
    candidaturas = (
        Candidatura.objects
        .filter(freelancer=perfil)
        .select_related('vaga__empresa__user')
        .order_by('-vaga__data_hora')
    )
    if status in dict(Candidatura.STATUS_CHOICES):
        candidaturas = candidaturas.filter(status=status)
    return candidaturas


@login_required(login_url='login')
def dashboard_freelancer(request):
    perfil = _perfil_freelancer(request)
    if not perfil:
        return HttpResponseForbidden('Acesso exclusivo para freelancers.')

    status_filter = request.GET.get('status', '')
    candidaturas = _candidaturas_do_freelancer(perfil, status_filter)[:8]

    context = {
        'perfil': perfil,
        'servicos_disponiveis': Servico.objects.filter(status='aberta').count(),
        'total_candidaturas': Candidatura.objects.filter(freelancer=perfil).count(),
        'candidaturas_aceitas': Candidatura.objects.filter(
            freelancer=perfil,
            status='aceita',
        ).count(),
        'total_avaliacoes': Avaliacao.objects.filter(
            usuario=perfil,
            tipo='freelancer',
        ).count(),
        'candidaturas': candidaturas,
        'status_filter': status_filter,
    }
    return render(request, 'perfis/freelancer/dashboard.html', context)


@login_required(login_url='login')
def encontrar_servicos(request):
    perfil = _perfil_freelancer(request)
    if not perfil:
        return HttpResponseForbidden('Acesso exclusivo para freelancers.')

    servicos = (
        Servico.objects
        .filter(status='aberta')
        .select_related('empresa__user')
        .annotate(total_candidatos=Count('candidaturas'))
    )

    palavra = request.GET.get('q', '').strip()
    empresa = request.GET.get('empresa', '').strip()
    valor_maximo = request.GET.get('valor_maximo', '').strip()
    data = request.GET.get('data', '').strip()
    ordenacao = request.GET.get('ordenacao', 'recentes')

    if palavra:
        servicos = servicos.filter(
            Q(nome__icontains=palavra) | Q(descricao__icontains=palavra)
        )
    if empresa:
        servicos = servicos.filter(
            Q(empresa__user__first_name__icontains=empresa)
            | Q(empresa__user__last_name__icontains=empresa)
            | Q(empresa__user__username__icontains=empresa)
        )
    if valor_maximo:
        try:
            servicos = servicos.filter(valor_hora__lte=Decimal(valor_maximo))
        except InvalidOperation:
            valor_maximo = ''
    if data:
        try:
            data_filtro = datetime.strptime(data, '%Y-%m-%d').date()
            servicos = servicos.filter(data_hora__date=data_filtro)
        except ValueError:
            data = ''

    ordenacoes = {
        'recentes': '-data_hora',
        'maior_valor': '-valor_hora',
        'menor_valor': 'valor_hora',
    }
    servicos = servicos.order_by(ordenacoes.get(ordenacao, '-data_hora'))

    candidaturas = {
        candidatura.vaga_id: candidatura
        for candidatura in Candidatura.objects.filter(
            freelancer=perfil,
            vaga__in=servicos,
        )
    }
    for servico in servicos:
        servico.candidatura_atual = candidaturas.get(servico.id)

    return render(request, 'perfis/freelancer/encontrar_servicos.html', {
        'perfil': perfil,
        'servicos': servicos,
        'palavra': palavra,
        'empresa_filtro': empresa,
        'valor_maximo': valor_maximo,
        'data_filtro': data,
        'ordenacao': ordenacao,
    })


@login_required(login_url='login')
def detalhe_servico_freelancer(request, servico_id):
    perfil = _perfil_freelancer(request)
    if not perfil:
        return HttpResponseForbidden('Acesso exclusivo para freelancers.')

    servico = get_object_or_404(
        Servico.objects.select_related('empresa__user').annotate(
            total_candidatos=Count('candidaturas')
        ),
        id=servico_id,
    )
    candidatura = Candidatura.objects.filter(
        vaga=servico,
        freelancer=perfil,
    ).first()
    avaliacao_empresa = Avaliacao.objects.filter(
        servico=servico,
        usuario=servico.empresa,
        tipo='servico',
    ).first()

    if servico.status != 'aberta' and not candidatura:
        return HttpResponseForbidden('Este serviço não está mais disponível.')

    return render(request, 'perfis/freelancer/detalhe_servico.html', {
        'perfil': perfil,
        'servico': servico,
        'candidatura': candidatura,
        'avaliacao_empresa': avaliacao_empresa,
    })


@login_required(login_url='login')
@require_POST
def candidatar_servico(request, servico_id):
    perfil = _perfil_freelancer(request)
    if not perfil:
        return HttpResponseForbidden('Apenas freelancers podem se candidatar.')

    servico = get_object_or_404(Servico, id=servico_id)
    if servico.status != 'aberta':
        return HttpResponseForbidden('Este serviço não aceita mais candidaturas.')

    candidatura, criada = Candidatura.objects.get_or_create(
        vaga=servico,
        freelancer=perfil,
        defaults={'status': 'pendente'},
    )
    if criada:
        messages.success(request, 'Candidatura enviada com sucesso.')
    else:
        messages.info(request, 'Você já se candidatou a este serviço.')
    return redirect('detalhe_servico_freelancer', servico.id)


@login_required(login_url='login')
def minhas_candidaturas(request):
    perfil = _perfil_freelancer(request)
    if not perfil:
        return HttpResponseForbidden('Acesso exclusivo para freelancers.')

    status_filter = request.GET.get('status', '')
    base = Candidatura.objects.filter(freelancer=perfil)
    return render(request, 'perfis/freelancer/candidaturas.html', {
        'perfil': perfil,
        'candidaturas': _candidaturas_do_freelancer(perfil, status_filter),
        'status_filter': status_filter,
        'total': base.count(),
        'pendentes': base.filter(status='pendente').count(),
        'aceitas': base.filter(status='aceita').count(),
        'rejeitadas': base.filter(status='rejeitada').count(),
    })


@login_required(login_url='login')
def avaliacoes_freelancer(request):
    perfil = _perfil_freelancer(request)
    if not perfil:
        return HttpResponseForbidden('Acesso exclusivo para freelancers.')

    avaliacoes = (
        Avaliacao.objects
        .filter(usuario=perfil, tipo='freelancer')
        .select_related('servico')
        .order_by('-criado_em')
    )
    resumo = avaliacoes.aggregate(media=Avg('nota'), total=Count('id'))
    return render(request, 'perfis/freelancer/avaliacoes.html', {
        'perfil': perfil,
        'avaliacoes': avaliacoes,
        'nota_media': resumo['media'],
        'total_avaliacoes': resumo['total'],
    })


@login_required(login_url='login')
def habilidades_freelancer(request):
    perfil = _perfil_freelancer(request)
    if not perfil:
        return HttpResponseForbidden('Acesso exclusivo para freelancers.')

    pesquisa = request.GET.get('q', '').strip()
    resultados = Habilidade.objects.none()
    if pesquisa:
        resultados = Habilidade.objects.filter(
            descricao__icontains=pesquisa
        ).order_by('descricao')[:12]

    if request.method == 'POST':
        descricao = request.POST.get('descricao', '').strip()
        if not descricao:
            messages.error(request, 'Informe uma habilidade.')
        else:
            habilidade = Habilidade.objects.filter(
                descricao__iexact=descricao
            ).first()
            if not habilidade:
                habilidade = Habilidade.objects.create(descricao=descricao)
            _, criada = HabilidadeUsuario.objects.get_or_create(
                usuario=perfil,
                habilidade=habilidade,
            )
            if criada:
                messages.success(request, 'Habilidade adicionada.')
            else:
                messages.info(request, 'Esta habilidade já está no seu perfil.')
        return redirect('habilidades_freelancer')

    return render(request, 'perfis/freelancer/habilidades.html', {
        'perfil': perfil,
        'habilidades_usuario': perfil.habilidades_usuario.select_related(
            'habilidade'
        ).order_by('habilidade__descricao'),
        'pesquisa': pesquisa,
        'resultados': resultados,
    })


@login_required(login_url='login')
@require_POST
def remover_habilidade_freelancer(request, habilidade_usuario_id):
    perfil = _perfil_freelancer(request)
    if not perfil:
        return HttpResponseForbidden('Acesso exclusivo para freelancers.')

    habilidade_usuario = get_object_or_404(
        HabilidadeUsuario,
        id=habilidade_usuario_id,
        usuario=perfil,
    )
    habilidade_usuario.delete()
    messages.success(request, 'Habilidade removida.')
    return redirect('habilidades_freelancer')


@login_required(login_url='login')
def perfil_freelancer(request):
    perfil = _perfil_freelancer(request)
    if not perfil:
        return HttpResponseForbidden('Acesso exclusivo para freelancers.')

    return render(request, 'perfis/freelancer/perfil.html', {
        'perfil': perfil,
        'habilidades_usuario': perfil.habilidades_usuario.select_related(
            'habilidade'
        ).order_by('habilidade__descricao'),
    })


@login_required(login_url='login')
def editar_perfil_freelancer(request):
    perfil = _perfil_freelancer(request)
    if not perfil:
        return HttpResponseForbidden('Acesso exclusivo para freelancers.')

    conta_form = ContaForm(request.POST or None, instance=request.user)
    perfil_form = PerfilForm(request.POST or None, instance=perfil)
    if request.method == 'POST' and conta_form.is_valid() and perfil_form.is_valid():
        conta_form.save()
        perfil_form.save()
        messages.success(request, 'Perfil atualizado com sucesso.')
        return redirect('perfil_freelancer')

    return render(request, 'perfis/freelancer/editar_perfil.html', {
        'perfil': perfil,
        'conta_form': conta_form,
        'perfil_form': perfil_form,
    })


@login_required(login_url='login')
def configuracoes_freelancer(request):
    perfil = _perfil_freelancer(request)
    if not perfil:
        return HttpResponseForbidden('Acesso exclusivo para freelancers.')

    conta_form = ContaForm(instance=request.user)
    perfil_form = PerfilForm(instance=perfil)
    senha_form = PasswordChangeForm(request.user)
    form_type = request.POST.get('form_type')

    if request.method == 'POST' and form_type == 'conta':
        conta_form = ContaForm(request.POST, instance=request.user)
        perfil_form = PerfilForm(request.POST, instance=perfil)
        if conta_form.is_valid() and perfil_form.is_valid():
            conta_form.save()
            perfil_form.save()
            messages.success(request, 'Dados da conta atualizados.')
            return redirect('configuracoes_freelancer')

    if request.method == 'POST' and form_type == 'senha':
        senha_form = PasswordChangeForm(request.user, request.POST)
        if senha_form.is_valid():
            user = senha_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Senha alterada com sucesso.')
            return redirect('configuracoes_freelancer')

    for field in senha_form.fields.values():
        field.widget.attrs['class'] = (
            'w-full rounded-2xl border border-purple-200 bg-white px-4 py-3 '
            'outline-none focus:border-purple-500 focus:ring-4 focus:ring-purple-100'
        )

    return render(request, 'perfis/freelancer/configuracoes.html', {
        'perfil': perfil,
        'conta_form': conta_form,
        'perfil_form': perfil_form,
        'senha_form': senha_form,
        'form_type': form_type,
    })
