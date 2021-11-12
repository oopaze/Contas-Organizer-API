from datetime import timedelta
from decimal import Decimal

from django.db import models

from core.models import TimeStampedModel


class Conta(TimeStampedModel):
    CARTAO = 'cartao'
    PRAZO = 'a_prazo'
    A_VISTA = 'a_vista'

    METODOS_PAGAMENTO = (
        (CARTAO, 'Cartão'),
        (PRAZO, 'A Prazo'),
        (A_VISTA, 'À Vista'),
    )

    produto = models.CharField("Produto", max_length=100)
    comprador = models.CharField("Comprador", max_length=100)
    metodo_de_pagamento = models.CharField(
        'Método de Pagamento', choices=METODOS_PAGAMENTO, max_length=20
    )
    pago = models.BooleanField('Pago?', default=False)
    loja = models.CharField("Loja", max_length=100)
    valor = models.DecimalField('Valor', decimal_places=2, max_digits=12)

    data_de_pagamento = models.DateField("Data de Pagamento")
    parcelas = models.PositiveIntegerField('Parcelas', default=1)

    owner = models.ForeignKey(
        'auth.User', on_delete=models.SET_NULL, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        is_creating = False
        if self._state.adding:
            is_creating = True

        instance = super().save(*args, **kwargs)

        if is_creating:
            self.pago = self.metodo_de_pagamento == self.A_VISTA
            self.save()

            self.create_parcelas()

        return instance

    def create_parcelas(self):
        for i in range(0, self.parcelas):
            Parcela.objects.create(
                numero_parcela=i + 1,
                data_de_pagamento=self.data_de_pagamento + timedelta(days=i * 30),
                conta=self,
                valor=Decimal(round(self.valor / self.parcelas, 2)),
                owner=self.owner,
            )


class Parcela(TimeStampedModel):
    conta = models.ForeignKey('Conta', on_delete=models.CASCADE)
    valor = models.DecimalField('Valor', decimal_places=2, max_digits=12)
    numero_parcela = models.PositiveIntegerField('Numero da Parcela')
    data_de_pagamento = models.DateField("Data de Pagamento")

    owner = models.ForeignKey(
        'auth.User', on_delete=models.SET_NULL, null=True, blank=True
    )
