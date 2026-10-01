from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group, User as Usuario
from login.utils import verificar_grupo
from django.core.exceptions import PermissionDenied
from login.utils import verificar_grupo
# Create your views here.



@login_required
def painel_principal(request):
    # Clientes não têm permissão para acessar o dashboard interno
    if verificar_grupo(request.user, 'cliente'):
        raise PermissionDenied
    
    contexto = {
        'usuarios': Usuario.objects.all()
    }
    return render(request, 'painel/home.html', contexto)


@login_required
def view_administrador(request):
    if not verificar_grupo(request.user, 'administradores'):
        raise PermissionDenied

    if request.method == 'POST':
        usuarios = Usuario.objects.all()

        for usuario in usuarios:
            novo_grupo_id = request.POST.get(f'grupo_usuario_{usuario.id}')
            if novo_grupo_id:
                try:
                    grupo = Group.objects.get(id=novo_grupo_id)
                    usuario.groups.clear()
                    usuario.groups.add(grupo)
                except Group.DoesNotExist:
                    pass

        return redirect('view_administrador')

    contexto = {
        'usuarios': Usuario.objects.all(),
        'grupos': Group.objects.all()
    }
    return render(request, 'painel/administrador.html', contexto)


@login_required
def view_diretoria(request):
    if not verificar_grupo(request.user, 'diretoria'):
        raise PermissionDenied
    return render(request, 'painel/diretoria.html')


@login_required
def view_gerencia_geral(request):
    if not verificar_grupo(request.user, 'gerencia_geral'):
        raise PermissionDenied
    return render(request, 'painel/gerencia_geral.html')


@login_required
def view_gerencia(request):
    if not verificar_grupo(request.user, 'gerencia'):
        raise PermissionDenied
    return render(request, 'painel/gerencia.html')


@login_required
def view_supervisao(request):
    if not verificar_grupo(request.user, 'supervisao'):
        raise PermissionDenied
    return render(request, 'painel/supervisao.html')


@login_required
def view_atendente(request):
    if not verificar_grupo(request.user, 'atendente'):
        raise PermissionDenied
    return render(request, 'painel/atendente.html')


@login_required
def view_caixa(request):
    if not verificar_grupo(request.user, 'caixa'):
        raise PermissionDenied
    return render(request, 'painel/caixa.html')