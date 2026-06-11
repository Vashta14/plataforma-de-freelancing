from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Avg, Count, Q

from .forms import ContaForm, LoginForm, PerfilForm, RegistroForm
from .models import Perfil
from servicos.models import Servico
from candidaturas.models import Candidatura
from django.shortcuts import get_object_or_404
from avaliacoes.models import Avaliacao


def landing_page(request):
    return render(request, 'perfis/landing.html')


def register(request, tipo=None):
    if tipo not in ('freelancer', 'empresa'):
        tipo = None

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Redirecionar baseado no tipo de usuário
            if user.perfil.tipo == 'empresa':
                return redirect('dashboard_empresa')
            else:
                return redirect('dashboard_freelancer')
    else:
        form = RegistroForm(initial={'tipo': tipo})
        if tipo:
            form.fields['tipo'].widget = form.fields['tipo'].hidden_widget()

    return render(request, 'perfis/auth/register.html', {
        'form': form,
        'tipo_escolhido': tipo,
    })


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirecionar baseado no tipo de usuário
            if user.perfil.tipo == 'empresa':
                return redirect('dashboard_empresa')
            else:
                return redirect('dashboard_freelancer')
    else:
        form = LoginForm()

    return render(request, 'perfis/auth/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('landing')


@login_required(login_url='login')
def dashboard_empresa(request):
    try:
        perfil = request.user.perfil
    except Perfil.DoesNotExist:
        return HttpResponseForbidden('Acesso negado. Perfil não encontrado.')

    if perfil.tipo != 'empresa':
        return HttpResponseForbidden('Acesso negado. Apenas empresas podem acessar este dashboard.')

    servicos = (
        Servico.objects
        .filter(empresa=perfil)
        .annotate(total_candidaturas=Count('candidaturas'))
        .order_by('-data_hora')
    )
    status_filter = request.GET.get('status')
    if status_filter in dict(Servico.STATUS_CHOICES):
        servicos = servicos.filter(status=status_filter)

    search_query = request.GET.get('q', '').strip()
    if search_query:
        servicos = servicos.filter(
            Q(nome__icontains=search_query)
            | Q(descricao__icontains=search_query)
            | Q(duracao__icontains=search_query)
        )

    total_servicos = Servico.objects.filter(empresa=perfil).count()
    abertos = Servico.objects.filter(empresa=perfil, status='aberta').count()
    finalizados = Servico.objects.filter(empresa=perfil, status='finalizado').count()
    cancelados = Servico.objects.filter(empresa=perfil, status='cancelada').count()

    context = {
        'perfil': perfil,
        'total_servicos': total_servicos,
        'abertos': abertos,
        'finalizados': finalizados,
        'cancelados': cancelados,
        'servicos': servicos,
        'status_filter': status_filter,
        'search_query': search_query,
        'status_choices': Servico.STATUS_CHOICES,
    }

    return render(request, 'perfis/empresa/dashboard.html', context)


@login_required(login_url='login')
def avaliacoes_empresa(request):
    try:
        perfil = request.user.perfil
    except Perfil.DoesNotExist:
        return HttpResponseForbidden('Acesso negado. Perfil não encontrado.')

    if perfil.tipo != 'empresa':
        return HttpResponseForbidden('Acesso negado. Apenas empresas podem acessar esta página.')

    avaliacoes = (
        Avaliacao.objects
        .filter(usuario=perfil, tipo='servico')
        .select_related('servico')
        .order_by('-criado_em')
    )
    resumo = avaliacoes.aggregate(media=Avg('nota'), total=Count('id'))

    return render(request, 'perfis/empresa/avaliacoes.html', {
        'perfil': perfil,
        'avaliacoes': avaliacoes,
        'nota_media': resumo['media'],
        'total_avaliacoes': resumo['total'],
    })


@login_required(login_url='login')
def perfil_empresa(request):
    try:
        perfil = request.user.perfil
    except Perfil.DoesNotExist:
        return HttpResponseForbidden('Acesso negado. Perfil não encontrado.')

    if perfil.tipo != 'empresa':
        return HttpResponseForbidden('Acesso negado. Apenas empresas podem acessar esta página.')

    total_servicos = Servico.objects.filter(empresa=perfil).count()
    total_candidaturas = Candidatura.objects.filter(vaga__empresa=perfil).count()
    total_avaliacoes = Avaliacao.objects.filter(
        usuario=perfil,
        tipo='servico',
    ).count()

    return render(request, 'perfis/empresa/perfil.html', {
        'perfil': perfil,
        'total_servicos': total_servicos,
        'total_candidaturas': total_candidaturas,
        'total_avaliacoes': total_avaliacoes,
    })


@login_required(login_url='login')
def configuracoes_empresa(request):
    try:
        perfil = request.user.perfil
    except Perfil.DoesNotExist:
        return HttpResponseForbidden('Acesso negado. Perfil não encontrado.')

    if perfil.tipo != 'empresa':
        return HttpResponseForbidden('Acesso negado. Apenas empresas podem acessar esta página.')

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
            messages.success(request, 'Dados da empresa atualizados.')
            return redirect('configuracoes_empresa')

    if request.method == 'POST' and form_type == 'senha':
        senha_form = PasswordChangeForm(request.user, request.POST)
        if senha_form.is_valid():
            user = senha_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Senha alterada com sucesso.')
            return redirect('configuracoes_empresa')

    for field in senha_form.fields.values():
        field.widget.attrs['class'] = (
            'w-full rounded-2xl border border-purple-200 bg-white px-4 py-3 '
            'outline-none focus:border-purple-500 focus:ring-4 focus:ring-purple-100'
        )

    return render(request, 'perfis/empresa/configuracoes.html', {
        'perfil': perfil,
        'conta_form': conta_form,
        'perfil_form': perfil_form,
        'senha_form': senha_form,
    })


@login_required(login_url='login')
def visualizar_perfil_freelancer(request, perfil_id):
    try:
        perfil = request.user.perfil
    except Perfil.DoesNotExist:
        return HttpResponseForbidden('Acesso negado. Perfil não encontrado.')

    if perfil.tipo != 'empresa':
        return HttpResponseForbidden('Acesso negado. Apenas empresas podem acessar este recurso.')

    freelancer = get_object_or_404(Perfil, id=perfil_id)
    servico_id = request.GET.get('servico')

    habilidades = freelancer.habilidades_usuario.select_related('habilidade').all()
    avaliacoes = Avaliacao.objects.filter(usuario=freelancer, tipo='freelancer').order_by('-criado_em')
    show_phone = False
    if servico_id:
        show_phone = Candidatura.objects.filter(vaga_id=servico_id, freelancer=freelancer, status='aceita').exists()

    return render(request, 'perfis/empresa/perfil_freelancer.html', {
        'freelancer': freelancer,
        'habilidades': habilidades,
        'avaliacoes': avaliacoes,
        'servico_id': servico_id,
        'show_phone': show_phone,
    })

