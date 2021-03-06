from django.urls import include, path
from rest_framework import routers

from .api import viewsets

router = routers.DefaultRouter()

router.register('kit-lanches', viewsets.KitLancheViewSet,
                basename='kit-lanches')

router.register('solicitacoes-kit-lanche-avulsa', viewsets.SolicitacaoKitLancheAvulsaViewSet,
                basename='solicitacao-kit-lanche-avulsa')

router.register('solicitacoes-kit-lanche-unificada', viewsets.SolicitacaoKitLancheUnificadaViewSet,
                basename='solicitacao-kit-lanche-unificada')

urlpatterns = [
    path('', include(router.urls))
]
