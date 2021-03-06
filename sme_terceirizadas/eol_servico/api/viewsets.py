from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from ..utils import get_informacoes_usuario


class DadosUsuarioEOLViewSet(ViewSet):
    lookup_field = 'registro_funcional'
    permission_classes = (AllowAny,)

    def retrieve(self, request, registro_funcional=None):
        response = get_informacoes_usuario(registro_funcional)
        if response.status_code == status.HTTP_200_OK:
            response = response.json()
            if not isinstance(response, dict):
                return Response({'detail': f'{response}'})  # a API do eol retorna 200 e um array com str de erro
            for result in response['results']:
                result.pop('cd_cpf_pessoa')
            return Response(response['results'])
        else:
            return Response({'detail': 'Request de API externa falhou'})
