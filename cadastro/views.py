from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
import uuid
from django.contrib.auth.models import Group, User
from django.contrib.auth.views import redirect_to_login




def cadastro(request):
    if request.method == "POST":
        username = request.POST.get("usuario")
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        confirmar_senha = request.POST.get("confirmar_senha")

        # --- VALIDAÇÕES ---
        if senha != confirmar_senha:
            messages.error(request, "As senhas não coincidem.")
            return render(request, "cadastro/cadastro.html")

        if len(senha) < 8:
            messages.error(request, "A senha deve ter pelo menos 8 caracteres.")
            return render(request, "cadastro/cadastro.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Este e-mail já está cadastrado.")
            return render(request, "cadastro/cadastro.html")

        # --- CRIAÇÃO DO USUÁRIO ---
        username_unico = uuid.uuid4().hex[:30]

        user = User.objects.create_user(
            username=username_unico,
            email=email,
            password=senha,
            first_name=username,
            is_active=False,
        )
        
        # Adiciona ao grupo 'cliente' automaticamente (cria o grupo se não existir)
        grupo_cliente, _ = Group.objects.get_or_create(name='cliente')
        user.groups.add(grupo_cliente)
        # --- ENVIO DO LINK DE ATIVAÇÃO ---
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        relative_link = reverse("ativar_conta", kwargs={"uidb64": uid, "token": token})
        
        # Detecta protocolo (http ou https) e domínio automaticamente (localhost:8000 em dev)
        protocolo = "https" if request.is_secure() else "http"
        domain = get_current_site(request).domain
        activation_url = f"{protocolo}://{domain}{relative_link}"

        assunto = "Confirme seu e-mail de cadastro"
        mensagem = (
            f"Olá, {user.first_name}!\n\n"
            f"Por favor, clique no link abaixo para ativar sua conta:\n\n"
            f"{activation_url}\n\n"
            f"Se você não solicitou este cadastro, ignore este e-mail."
        )
        
        send_mail(assunto, mensagem, None, [user.email], fail_silently=False)

        messages.success(
            request,
            "Cadastro realizado! Enviamos um link de ativação para o seu e-mail.",
        )
        return redirect("login")

    return render(request, "cadastro/cadastro.html")


def ativar_conta(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Sua conta foi ativada com sucesso! Você já pode fazer login.")
    else:
        messages.error(request, "O link de ativação é inválido ou expirou.")
        
    return redirect("login")