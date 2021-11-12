from rest_framework import serializers

from contas.models import Conta, Parcela


class ContaSerializer(serializers.ModelSerializer):
    data_de_pagamento = serializers.DateField(
        format="%d/%m/%Y", input_formats=['%d/%m/%Y', '%d-%m-%Y']
    )

    class Meta:
        model = Conta
        exclude = ('create_at', 'update_at')


class ParcelaSerializer(serializers.ModelSerializer):
    data_de_pagamento = serializers.DateField(
        format="%d/%m/%Y", input_formats=['%d/%m/%Y', '%d-%m-%Y']
    )
    owner = serializers.SerializerMethodField()
    data_de_compra = serializers.SerializerMethodField()
    comprador = serializers.SerializerMethodField()
    produto = serializers.SerializerMethodField()

    def get_owner(self, instance):
        return instance.owner.username

    def get_data_de_compra(self, instance):
        return f"{instance.conta.create_at: %d/%m/%Y}"

    def get_produto(self, instance):
        return instance.conta.produto

    def get_comprador(self, instance):
        return instance.conta.comprador

    class Meta:
        model = Parcela
        exclude = ('create_at', 'update_at')
