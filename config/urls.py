"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from servicos.views import lista_de_servicos, criar_servico, editar_servico, detalhe_servico, cancelar_servico, finalizar_servico
from perfis.views import (
    avaliacoes_empresa,
    dashboard_empresa,
    landing_page,
    login_view,
    logout_view,
    configuracoes_empresa,
    perfil_empresa,
    register,
)
from candidaturas.views import candidaturas, aceitar_candidatura, rejeitar_candidatura
from perfis.views import visualizar_perfil_freelancer
from avaliacoes.views import avaliar_empresa, avaliar_freelancer
from perfis.freelancer_views import (
    avaliacoes_freelancer,
    candidatar_servico,
    configuracoes_freelancer,
    dashboard_freelancer,
    detalhe_servico_freelancer,
    editar_perfil_freelancer,
    encontrar_servicos,
    habilidades_freelancer,
    minhas_candidaturas,
    perfil_freelancer,
    remover_habilidade_freelancer,
)

urlpatterns = [
    path('', landing_page, name='landing'),
    path('cadastro/', register, name='register_generic'),
    path('cadastro/<str:tipo>/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/empresa/', dashboard_empresa, name='dashboard_empresa'),
    path('dashboard/empresa/avaliacoes/', avaliacoes_empresa, name='avaliacoes_empresa'),
    path('dashboard/empresa/perfil/', perfil_empresa, name='perfil_empresa'),
    path('dashboard/empresa/configuracoes/', configuracoes_empresa, name='configuracoes_empresa'),
    path('dashboard/freelancer/', dashboard_freelancer, name='dashboard_freelancer'),
    path('freelancer/servicos/', encontrar_servicos, name='encontrar_servicos'),
    path('freelancer/servicos/<uuid:servico_id>/', detalhe_servico_freelancer, name='detalhe_servico_freelancer'),
    path('freelancer/servicos/<uuid:servico_id>/candidatar/', candidatar_servico, name='candidatar_servico'),
    path('freelancer/candidaturas/', minhas_candidaturas, name='minhas_candidaturas'),
    path('freelancer/avaliacoes/', avaliacoes_freelancer, name='avaliacoes_freelancer'),
    path('freelancer/habilidades/', habilidades_freelancer, name='habilidades_freelancer'),
    path('freelancer/habilidades/<uuid:habilidade_usuario_id>/remover/', remover_habilidade_freelancer, name='remover_habilidade_freelancer'),
    path('freelancer/perfil/', perfil_freelancer, name='perfil_freelancer'),
    path('freelancer/perfil/editar/', editar_perfil_freelancer, name='editar_perfil_freelancer'),
    path('freelancer/configuracoes/', configuracoes_freelancer, name='configuracoes_freelancer'),
    path('servicos/', lista_de_servicos, name='lista_de_servicos'),
    path('servicos/criar/', criar_servico, name='criar_servico'),
    path('servicos/<uuid:servico_id>/editar/', editar_servico, name='editar_servico'),
    path('servicos/<uuid:servico_id>/cancelar/', cancelar_servico, name='cancelar_servico'),
    path('servicos/<uuid:servico_id>/finalizar/', finalizar_servico, name='finalizar_servico'),
    path('servicos/<uuid:servico_id>/', detalhe_servico, name='detalhe_servico'),
    path('candidaturas/', candidaturas, name='candidaturas'),
    path('candidaturas/<uuid:candidatura_id>/aceitar/', aceitar_candidatura, name='aceitar_candidatura'),
    path('candidaturas/<uuid:candidatura_id>/rejeitar/', rejeitar_candidatura, name='rejeitar_candidatura'),
    path('freelancers/<uuid:perfil_id>/', visualizar_perfil_freelancer, name='visualizar_perfil_freelancer'),
    path('avaliacoes/avaliar/<uuid:servico_id>/<uuid:perfil_id>/', avaliar_freelancer, name='avaliar_freelancer'),
    path('avaliacoes/empresa/<uuid:servico_id>/', avaliar_empresa, name='avaliar_empresa'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
