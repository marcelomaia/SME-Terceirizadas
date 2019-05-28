from typing import Any

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from sme_pratoaberto_terceirizadas.users.models import User
from sme_pratoaberto_terceirizadas.utils import send_notification, async_send_mass_html_mail
from .serializers import AlteracaoCardapioSerializer
from ..models import AlteracaoCardapio

cintia_qs = User.objects.filter(email='mmaia.cc@gmail.com')

emails = ['mmaia.cc@gmail.com', 'weslei.souza@amcom.com.br', 'cintia.ramos@amcom.com.br']


class AlteracaoCardapioViewSet(ModelViewSet):
    queryset = AlteracaoCardapio.objects.all()
    serializer_class = AlteracaoCardapioSerializer
    lookup_field = 'uuid'

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        response = super().create(request, *args, **kwargs)
        if response:
            short_desc = 'Alteração de cardápio solicitada'.format(response.data.get('id', None))

            send_notification(sender=request.user, recipients=cintia_qs,
                              short_desc=short_desc, long_desc=response.data)
            async_send_mass_html_mail(short_desc, str(response.data), None, emails)
        return response

    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        response = super().partial_update(request, *args, **kwargs)
        if response:
            alt_id = response.data.get('id', None)
            status = response.data.get('status', None)
            short_desc = 'Alteração de cardápio #{} atualizada para: {}'.format(
                alt_id, status)
            send_notification(sender=request.user, recipients=cintia_qs,
                              short_desc=short_desc, long_desc=response.data)
            async_send_mass_html_mail(short_desc, str(response.data), None, emails)
        return response

    @action(detail=False)
    def dre(self, request):
        return Response({'message': 'Diretoria regional'})

    @action(detail=False)
    def terceirizadas(self, request):
        return Response({'message': 'Empresa terceirizadas'})
