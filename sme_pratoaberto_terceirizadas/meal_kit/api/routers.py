from django.urls import path, include
from rest_framework import routers
from .viewsets import MealKitViewSet, OrderMealKitViewSet, SolicitacaoUnificadaViewSet

router = routers.DefaultRouter()

router.register('kit-lanche', MealKitViewSet, base_name='meal_kit')
router.register('solicitar-kit-lanche', OrderMealKitViewSet, basename='solicitar_kit_lanche')
router.register('solicitacao-unificada', SolicitacaoUnificadaViewSet, basename='solicitacao_unificada')

urlpatterns = [
    path('', include(router.urls))
]
