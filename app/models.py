# app/models.py
from django.db import models

class Pedido(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Aguardando Pagamento'),
        ('pago', 'Pago'),
        ('cancelado', 'Cancelado'),
    ]

    METODOS_PAGAMENTO = [
        ('pix', 'PIX'),
        ('cartao', 'Cartão de Crédito'),
        ('boleto', 'Boleto Bancário'),
    ]

    usuario = models.CharField(max_length=150)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    metodo_pagamento = models.CharField(max_length=20, choices=METODOS_PAGAMENTO, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario} ({self.get_status_display()})"


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    nome = models.CharField(max_length=200)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.preco * self.quantidade