import random
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

def gerar_codigo():
    return f"{random.randint(100000, 999999)}"

class TwoFactorCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mfa_codes')
    code = models.CharField(max_length=6, default=gerar_codigo)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        # Válido por 5 minutos e se ainda não foi utilizado
        expiracao = self.created_at + timedelta(minutes=5)
        return not self.is_used and timezone.now() <= expiracao

    def mark_as_used(self):
        self.is_used = True
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.code}"