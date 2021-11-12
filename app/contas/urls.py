from django.urls import path

from .views import ContaCreateAPIView, ParcelaListAPIView


app_name = 'contas'

urlpatterns = [
    path('parcelas/', ParcelaListAPIView.as_view(), name="parcela_list"),
    path('conta/', ContaCreateAPIView.as_view(), name="conta_create"),
]
