# Plataforma de Freelancing

Projeto Django simples para gerenciar perfis, habilidades, serviços, candidaturas e avaliações.

## Visão geral

Apps principais:
- `perfis` — perfis de `empresa` e `freelancer` (liga ao `User` do Django)
- `habilidades` — catálogo de habilidades e vínculo com perfis
- `servicos` — vagas/serviços publicados por empresas
- `candidaturas` — candidaturas de freelancers a serviços
- `avaliacoes` — avaliações de serviços/freelancers

O painel administrativo do Django é o ponto de acesso principal por enquanto (`/admin/`).

## Pré-requisitos

- Python 3.11+
- Docker & Docker Compose (opcional, recomendado)

## Instalação local (sem Docker)

1. Crie e ative um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Instale dependências:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

3. Aplique migrações e crie superuser:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

4. Rode o servidor:

```bash
python manage.py runserver
```

Abra `http://127.0.0.1:8000/admin/` e faça login com o superuser.

## Usando Docker (recomendado para desenvolvimento)

1. Build e suba os containers:

```bash
docker-compose build
docker-compose up
```

2. Rodar em background:

```bash
docker-compose up -d
```

3. Criar superuser dentro do container:

```bash
docker-compose exec web python manage.py createsuperuser
```