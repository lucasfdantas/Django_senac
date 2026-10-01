from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from django.utils.http import url_has_allowed_host_and_scheme
from .models import TwoFactorCode
from .utils import verificar_grupo


@require_http_methods(["GET", "POST"])
def login_view(request):
    # Se já estiver autenticado e tentar acessar login, honra o next ou vai pro painel
    if request.user.is_authenticated:
        next_url = request.GET.get('next') or request.POST.get('next')
        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
            return redirect(next_url)
        return redirect('painel')

    # Captura o 'next' vindo da URL (?next=/carrinho/checkout/)
    next_url = request.GET.get('next') or request.POST.get('next')

    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        usuario_objeto = User.objects.filter(email=email).first()

        if usuario_objeto:
            if not usuario_objeto.is_active and usuario_objeto.check_password(senha):
                messages.error(request, "Sua conta ainda não foi ativada. Verifique seu e-mail.")
                return render(request, "login/login.html", {'next': next_url})

            user = authenticate(request, username=usuario_objeto.username, password=senha)

            if user is not None:
                TwoFactorCode.objects.filter(user=user, is_used=False).update(is_used=True)
                two_factor_obj = TwoFactorCode.objects.create(user=user)

                domain = get_current_site(request).domain
                from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', f'no-reply@{domain}')

                send_mail(
                    subject=f'Código de Autenticação - {domain}',
                    message=f'Seu código de acesso é: {two_factor_obj.code}',
                    from_email=from_email,
                    recipient_list=[user.email],
                    fail_silently=False,
                )

                # Salva o usuário e o destino pretendido na sessão temporária
                request.session['pre_2fa_user_id'] = user.id
                if next_url:
                    request.session['login_next_url'] = next_url

                return redirect('mfa')

        messages.error(request, "E-mail ou senha inválidos.")

    return render(request, 'login/login.html', {'next': next_url})

def mfa_view(request):
    user_id = request.session.get('pre_2fa_user_id')

    if not user_id:
        return redirect('login')

    if request.method == 'POST':
        code_input = request.POST.get('code', '').strip()

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return redirect('login')

        two_factor_obj = TwoFactorCode.objects.filter(
            user=user,
            code=code_input,
            is_used=False
        ).order_by('-created_at').first()

        if two_factor_obj and two_factor_obj.is_valid():
            two_factor_obj.mark_as_used()
            login(request, user)

            # Limpa ID temporário da sessão
            del request.session['pre_2fa_user_id']

            # Recupera a URL de retorno que estava salva
            next_url = request.session.pop('login_next_url', None)

            # Validação de segurança (Open Redirect Protection): 
            # Garante que a URL pertence ao mesmo domínio e não é um link externo malicioso
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)

            # Se não havia 'next', segue o fluxo natural de redirecionamento de painel
            return redirect('home')
        else:
            messages.error(request, 'Código inválido ou expirado. Tente novamente.')

    return render(request, 'login/mfa.html')
def logout_view(request):
    logout(request)
    return redirect('home')
@login_required
def painel_redirect(request):
    user = request.user

    # 1. Se for cliente, redireciona para a loja/home (não acessa painel)
    if verificar_grupo(user, 'cliente'):
        return redirect('home')  # ou 'loja_carrinho' ou 'meus_pedidos'

    # 2. Roteamento corporativo/administrativo
    grupos_rotas = [
        ('administradores', 'view_administrador'),
        ('diretoria', 'view_diretoria'),
        ('gerencia_geral', 'view_gerencia_geral'),
        ('gerencia', 'view_gerencia'),
        ('supervisao', 'view_supervisao'),
        ('atendente', 'view_atendente'),
        ('caixa', 'view_caixa'),
    ]

    for grupo, rota_name in grupos_rotas:
        if verificar_grupo(user, grupo):
            return redirect(rota_name)

    if user.is_superuser:
        return redirect('/admin/')

    # Se não for de nenhum grupo administrativo nem superuser
    raise PermissionDenied

@login_required
def painel_redirect(request):
    user = request.user

    # Roteamento baseado em grupos hierárquicos
    grupos_rotas = [
        ('administradores', 'view_administrador'),
        ('diretoria', 'view_diretoria'),
        ('gerencia_geral', 'view_gerencia_geral'),
        ('gerencia', 'view_gerencia'),
        ('supervisao', 'view_supervisao'),
        ('atendente', 'view_atendente'),
        ('caixa', 'view_caixa'),
    ]

    for grupo, rota_name in grupos_rotas:
        if verificar_grupo(user, grupo):
            return redirect(rota_name)

    # Superusuário sem grupo específico cai por padrão no admin
    if user.is_superuser:
        return redirect('/admin/')

    raise PermissionDenied