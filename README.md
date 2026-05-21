# Plataforma de Freelancing

Uma plataforma web para conectar freelancers e clientes, facilitando a contratação de serviços e gerenciamento de projetos.

## 📋 Sobre o Projeto

Este é um projeto Django que oferece um sistema completo para:
- Gerenciamento de perfis de usuários
- Cadastro e listagem de serviços
- Sistema de avaliações e ratings
- Gerenciamento de candidaturas
- Controle de habilidades profissionais

## 🎯 Aplicações Django Incluídas

- **avaliacoes**: Sistema de avaliações e ratings
- **candidaturas**: Gerenciamento de candidaturas a projetos
- **habilidades**: Cadastro e controle de habilidades dos freelancers
- **perfis**: Gerenciamento de perfis de usuários (freelancer e empresa)
- **servicos**: Listagem e gerenciamento de serviços

## 🛠️ Requisitos

- Python 3.8+
- Django 3.2+
- pip

## 📦 Instalação

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd plataforma-de-freelancing
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv
```

### 3. Ative o ambiente virtual
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 4. Instale as dependências
```bash
pip install django 
pip install django -unfold 
```

## 🚀 Como Executar

### Sem Docker

1. **Execute as migrações do banco de dados**
```bash
python manage.py migrate
```

2. **Crie um superusuário (admin)**
```bash
python manage.py createsuperuser
```

3. **Inicie o servidor de desenvolvimento**
```bash
python manage.py runserver
```

O servidor estará disponível em `http://127.0.0.1:8000`

## 👨‍💻 Desenvolvimento

### Criar migrations
```bash
python manage.py makemigrations
```

### Aplicar migrations
```bash
python manage.py migrate
```

### Acessar o painel admin
Vá para `http://127.0.0.1:8000/admin/` e faça login com suas credenciais de superusuário.

## 📁 Estrutura do Projeto

```
plataforma-de-freelancing/
├── config/                 # Configurações do projeto
├── avaliacoes/            # App de avaliações
├── candidaturas/          # App de candidaturas
├── habilidades/           # App de habilidades
├── perfis/                # App de perfis
├── servicos/              # App de serviços
├── manage.py              # Gerenciador do Django
├── .gitignore             # Arquivos ignorados pelo Git
└── README.md              # Este arquivo
```