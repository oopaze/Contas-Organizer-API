from datetime import date, datetime

from dateutil.relativedelta import relativedelta
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from contas.models import Conta, Parcela
from contas.serializers import ContaSerializer, ParcelaSerializer


class ContaCreateAPIView(CreateAPIView):
    model = Conta
    serializer_class = ContaSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        response = super().perform_create(serializer)
        serializer.instance.owner = self.request.user
        serializer.instance.parcela_set.update(owner=self.request.user)
        serializer.instance.save()
        return response


class ParcelaListAPIView(ListAPIView):
    model = Parcela
    permission_classes = [IsAuthenticated]
    serializer_class = ParcelaSerializer

    def get_queryset(self):
        today = date.today().replace(day=1)

        begin_next_month = today + relativedelta(months=+1)
        end_next_month = today + relativedelta(months=+2)

        return self.model.objects.filter(
            owner=self.request.user,
            data_de_pagamento__gte=begin_next_month,
            data_de_pagamento__lte=end_next_month,
        )
