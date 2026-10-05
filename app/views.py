from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import redirect_to_login
from django.db import transaction
from .models import Pedido, ItemPedido  
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


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


# def loja_carrinho(request):
#     if request.method == 'POST':
#         produto_id = request.POST.get('produto_id')
#         nome = request.POST.get('nome_produto')
#         preco = request.POST.get('preco_produto')
#         quantidade_vinda = request.POST.get('quantidade', 1)

#         # Onde a requisição começou (a própria página do catálogo)
#         origem = request.META.get('HTTP_REFERER', 'catalogo')

#         # Se campos obrigatórios estiverem vazios, apenas recarrega
#         if not produto_id or not preco or produto_id == 'None':
#             return redirect(origem)

#         try:
#             quantidade_vinda = int(quantidade_vinda)
#             if quantidade_vinda <= 0:
#                 quantidade_vinda = 1
#         except (ValueError, TypeError):
#             quantidade_vinda = 1

#         # Inicializa o carrinho na sessão se não existir
#         if 'carrinho' not in request.session:
#             request.session['carrinho'] = {}
            
#         carrinho = request.session['carrinho']
#         id_str = str(produto_id)

#         # Atualiza a quantidade ou insere novo item
#         if id_str in carrinho:
#             carrinho[id_str]['qtd'] = int(carrinho[id_str]['qtd']) + quantidade_vinda
#         else:
#             carrinho[id_str] = {
#                 'id': id_str,
#                 'nome': nome,
#                 'preco': preco,
#                 'qtd': quantidade_vinda
#             }

#         request.session['carrinho'] = carrinho
#         request.session.modified = True

#         # Mensagem flash informando que o produto foi adicionado
#         messages.success(request, f'"{nome}" foi adicionado ao seu carrinho!')

#         # Recarrega exatamente a mesma página em que o usuário estava
#         return redirect(origem)

#     return render(request, 'catalogo/catalogo.html')
def loja_carrinho(request):
    if request.method == 'POST':
        produto_id = request.POST.get('produto_id')
        nome = request.POST.get('nome_produto')
        preco = request.POST.get('preco_produto')
        quantidade_vinda = request.POST.get('quantidade', 1)

        # Detecta se a requisição veio via JavaScript (Fetch / AJAX)
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest' or \
                  'application/json' in request.headers.get('Accept', '')

        if not produto_id or not preco or produto_id == 'None':
            if is_ajax:
                return JsonResponse({'sucesso': False, 'erro': 'Dados inválidos'}, status=400)
            return redirect(request.META.get('HTTP_REFERER', 'catalogo'))

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

        # Incrementa quantidade ou insere o produto
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

        # Total de itens acumulados no carrinho para atualizar a navbar
        total_itens = sum(int(item['qtd']) for item in carrinho.values())

        # Se for chamada assíncrona, responde sem dar reload
        if is_ajax:
            return JsonResponse({
                'sucesso': True,
                'mensagem': f'"{nome}" foi adicionado ao seu carrinho!',
                'total_itens': total_itens
            })

        # Fallback tradicional caso o JavaScript esteja desativado
        messages.success(request, f'"{nome}" foi adicionado ao seu carrinho!')
        return redirect(request.META.get('HTTP_REFERER', 'catalogo'))

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

@login_required
def view_checkout(request):
    """Cria o pedido pendente no banco e redireciona direto para a escolha do pagamento"""
    carrinho = request.session.get('carrinho', {})

    if not carrinho:
        return redirect('catalogo')

    total = request.session.get('total_carrinho', 0.0)

    # Cria o pedido e esvazia o carrinho da sessão
    with transaction.atomic():
        pedido = Pedido.objects.create(
            usuario=request.user.username,
            total=total,
            status='pendente'
        )

        for item in carrinho.values():
            ItemPedido.objects.create(
                pedido=pedido,
                nome=item['nome'],
                preco=item['preco'],
                quantidade=item['qtd']
            )

        # Limpa o carrinho após gravar no banco
        request.session.pop('carrinho', None)
        request.session.pop('total_carrinho', None)
        request.session.modified = True

    return redirect('pagamento_pedido', pedido_id=pedido.id)
@login_required
def pagamento_pedido(request, pedido_id):
    """Tela onde o usuário seleciona Pix, Cartão ou Boleto"""
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user.username)

    # Se já foi pago, envia direto para a confirmação
    if pedido.status == 'pago':
        return redirect('sucesso_pedido', pedido_id=pedido.id)

    if request.method == 'POST':
        metodo = request.POST.get('metodo_pagamento')

        if metodo in ['pix', 'cartao', 'boleto']:
            pedido.metodo_pagamento = metodo
            # Simulação: se escolheu cartão, aprova na hora; se pix/boleto, fica pendente
            if metodo == 'cartao':
                pedido.status = 'pago'
            else:
                pedido.status = 'pendente'

            pedido.save()
            return redirect('sucesso_pedido', pedido_id=pedido.id)

    return render(request, 'pedidos/pagamento.html', {'pedido': pedido})


@login_required
def sucesso_pedido(request, pedido_id):
    """Tela final com resumo e detalhes da transação"""
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user.username)
    return render(request, 'pedidos/sucesso.html', {'pedido': pedido})