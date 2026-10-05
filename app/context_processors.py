# app/context_processors.py

def carrinho_context(request):
    carrinho = request.session.get('carrinho', {})
    total_itens = 0

    if isinstance(carrinho, dict):
        for item in carrinho.values():
            if isinstance(item, dict) and 'qtd' in item:
                try:
                    total_itens += int(item['qtd'])
                except (ValueError, TypeError):
                    pass

    return {
        'total_itens_carrinho': total_itens,
        'carrinho_badge': '99+' if total_itens > 99 else str(total_itens)
    }