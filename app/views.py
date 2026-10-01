from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import redirect_to_login
from django.db import transaction
from .models import Pedido, ItemPedido  
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import render, redirect
from django.contrib import messages



def home(request):
    # Caminho: templates/home/index.html
    context = {
        'titulo_secao': 'Destaques da Semana'
    }
    return render(request, 'home/index.html', context)

def catalogo(request):
    # Exemplo simulando dados vindos de um model
    produtos = [
        {'id': 1, 'nome': 'Produto A', 'preco': 99.90},
        {'id': 2, 'nome': 'Produto B', 'preco': 149.90},
    ]
    return render(request, 'catalogo/catalogo.html', {'produtos': produtos})

def contato(request):
    return render(request, 'contato/contato.html')

def sobre(request):
    return render(request, 'sobre/sobre.html')


def loja_carrinho(request):
    if request.method == 'POST':
        produto_id = request.POST.get('produto_id')
        nome = request.POST.get('nome_produto')
        preco = request.POST.get('preco_produto')
        quantidade_vinda = request.POST.get('quantidade', 1)

        # Onde a requisição começou (a própria página do catálogo)
        origem = request.META.get('HTTP_REFERER', 'catalogo')

        # Se campos obrigatórios estiverem vazios, apenas recarrega
        if not produto_id or not preco or produto_id == 'None':
            return redirect(origem)

        try:
            quantidade_vinda = int(quantidade_vinda)
            if quantidade_vinda <= 0:
                quantidade_vinda = 1
        except (ValueError, TypeError):
            quantidade_vinda = 1

        # Inicializa o carrinho na sessão se não existir
        if 'carrinho' not in request.session:
            request.session['carrinho'] = {}
            
        carrinho = request.session['carrinho']
        id_str = str(produto_id)

        # Atualiza a quantidade ou insere novo item
        if id_str in carrinho:
            carrinho[id_str]['qtd'] = int(carrinho[id_str]['qtd']) + quantidade_vinda
        else:
            carrinho[id_str] = {
                'id': id_str,
                'nome': nome,
                'preco': preco,
                'qtd': quantidade_vinda
            }

        request.session['carrinho'] = carrinho
        request.session.modified = True

        # Mensagem flash informando que o produto foi adicionado
        messages.success(request, f'"{nome}" foi adicionado ao seu carrinho!')

        # Recarrega exatamente a mesma página em que o usuário estava
        return redirect(origem)

    return render(request, 'catalogo/catalogo.html')


def lista_carrinho(request):
    compras = request.session.get('carrinho', {})
    # Remove chaves inválidas que possam ter entrado na sessão
    compras.pop(None, None)
    compras.pop('None', None)

    # Se o carrinho estiver vazio no carregamento inicial, volta para o catálogo
    if not compras and request.method == 'GET':
        return redirect('catalogo')

    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        acao = request.POST.get('acao')

        if item_id in compras:
            if acao == 'mais_item':
                compras[item_id]['qtd'] = int(compras[item_id]['qtd']) + 1
            elif acao == 'menos_item':
                compras[item_id]['qtd'] = int(compras[item_id]['qtd']) - 1
                if compras[item_id]['qtd'] <= 0:
                    del compras[item_id]

            request.session['carrinho'] = compras
            request.session.modified = True
            return redirect('lista_carrinho')

    # Calcula os totais
    total = 0.0
    for item in compras.values():
        if item.get('preco') is None or item.get('qtd') is None:
            continue
        try:
            total += float(item['preco']) * int(item['qtd'])
        except (ValueError, TypeError):
            continue

    request.session['total_carrinho'] = total
    request.session.modified = True

    contexto = {
        'carrinho': compras,
        'total': total
    }
    # Aponta para o arquivo renomeado dentro da pasta catalogo/
    return render(request, 'catalogo/lista_carrinho.html', contexto)

def view_checkout(request):
    if not request.user.is_authenticated:
        return redirect_to_login(request.get_full_path(), login_url='login')
    carrinho = request.session.get('carrinho')
    if not carrinho:
        return redirect('loja_carrinho')

    total = request.session.get('total_carrinho', 0.0)

    if not request.user.is_authenticated:
        return redirect_to_login(request.get_full_path(), login_url='login')

    if request.method == 'POST':
        with transaction.atomic():
            pedido = Pedido.objects.create(
                usuario=request.user.username,
                total=total
            )

            for item in carrinho.values():
                ItemPedido.objects.create(
                    pedido=pedido,
                    nome=item['nome'],
                    preco=item['preco'],
                    quantidade=item['qtd']
                )

            # Limpa carrinho da sessão
            request.session.pop('carrinho', None)
            request.session.pop('total_carrinho', None)
            request.session.modified = True

        return redirect('sucesso_pedido', pedido_id=pedido.id)

    contexto = {
        'carrinho': carrinho,
        'total_carrinho': total
    }
    return render(request, 'carrinho/checkout.html', contexto)


def sucesso_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'carrinho/sucesso.html', {'pedido': pedido})