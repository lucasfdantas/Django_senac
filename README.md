# Sistema Django Senac

Este projeto é uma aplicação web em Django para um sistema de loja/comércio com autenticação de usuários, cadastro, ativação por e-mail, autenticação em duas etapas (MFA), carrinho de compras e painel de gestão por perfil de usuário.

## Tecnologias

- Python
- Django 6.1.1
- SQLite
- HTML, CSS e JavaScript
- Templates do Django

## Funcionalidades principais

- Página inicial com destaque de produtos
- Catálogo de produtos
- Carrinho de compras em sessão
- Checkout com pedido e confirmação
- Cadastro de usuários
- Ativação de conta via e-mail
- Login com MFA (código temporário)
- Painel por perfil: administração, diretoria, gerência, supervisão, atendente e caixa
- Integração com Django Admin

## Estrutura do projeto

```text
django_senac/
├── app/
│   ├── templates/
│   ├── views.py
│   ├── models.py
│   └── ...
├── cadastro/
│   ├── templates/
│   ├── views.py
│   └── ...
├── login/
│   ├── templates/
│   ├── views.py
│   ├── utils.py
│   └── ...
├── painel/
│   ├── templates/
│   ├── views.py
│   └── ...
├── sistema/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── static/
├── templates/
├── manage.py
├── db.sqlite3
├── requeriments.txt
├── README.md
└── ...
```

## Requisitos

- Python 3.10+
- pip
- Ambiente virtual (recomendado)

## Configuração do ambiente

1. Acesse a pasta do projeto:

```bash
cd django_senac
```

2. Crie e ative um ambiente virtual:

```bash
python -m venv .venv
```

No Windows:

```bash
.venv\Scripts\activate
```

No Linux/macOS:

```bash
source .venv/bin/activate
```

3. Instale as dependências:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente necessárias para o projeto. O projeto usa `SECRET_KEY` e `DEBUG` nas configurações.

Exemplo:

```bash
set SECRET_KEY=sua_chave_secreta
set DEBUG=True
```

No Linux/macOS:

```bash
export SECRET_KEY=sua_chave_secreta
export DEBUG=True
```

## Banco de dados

Para criar o banco de dados e aplicar as migrações:

```bash
python manage.py migrate
```

## Executando o projeto

Inicie o servidor local:

```bash
python manage.py runserver
```

Acesse:

```text
http://127.0.0.1:8000/
```

## Criação de superusuário

Para acessar o painel administrativo do Django:

```bash
python manage.py createsuperuser
```

Em seguida, acesse:

```text
http://127.0.0.1:8000/admin/
```

## Fluxo de uso

- Usuário acessa a página inicial e navega pelo catálogo
- Faz cadastro na rota `/cadastro/`
- Recebe link de ativação por e-mail
- Realiza login e confirma código MFA
- Adiciona produtos ao carrinho
- Finaliza compra e recebe confirmação do pedido
- Usuários com grupos específicos têm acesso ao painel administrativo

## Observações

- O sistema usa SQLite em desenvolvimento, o que facilita testes locais.
- O envio de e-mails em produção pode exigir configuração SMTP e credenciais válidas.
- Em modo `DEBUG=True`, o Django usa o backend de e-mail de console; em produção, o projeto está preparado para SMTP.

## Licença

Este projeto foi desenvolvido para fins acadêmicos e de estudo.
