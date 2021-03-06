from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from xworkflows import InvalidTransitionError

from ...dados_comuns import constants
from ..models import (
    GrupoInclusaoAlimentacaoNormal,
    InclusaoAlimentacaoContinua,
    MotivoInclusaoContinua,
    MotivoInclusaoNormal
)
from .permissions import (
    PodeAprovarAlimentacaoContinuaDaEscolaPermission,
    PodeIniciarInclusaoAlimentacaoContinuaPermission
)
from .serializers import serializers, serializers_create


class MotivoInclusaoContinuaViewSet(ReadOnlyModelViewSet):
    lookup_field = 'uuid'
    queryset = MotivoInclusaoContinua.objects.all()
    serializer_class = serializers.MotivoInclusaoContinuaSerializer


class MotivoInclusaoNormalViewSet(ReadOnlyModelViewSet):
    lookup_field = 'uuid'
    queryset = MotivoInclusaoNormal.objects.all()
    serializer_class = serializers.MotivoInclusaoNormalSerializer


class GrupoInclusaoAlimentacaoNormalViewSet(ModelViewSet):
    lookup_field = 'uuid'
    queryset = GrupoInclusaoAlimentacaoNormal.objects.all()
    serializer_class = serializers.GrupoInclusaoAlimentacaoNormalSerializer

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return serializers_create.GrupoInclusaoAlimentacaoNormalCreationSerializer
        return serializers.GrupoInclusaoAlimentacaoNormalSerializer

    @action(detail=False, url_path=constants.SOLICITACOES_DO_USUARIO)
    def minhas_solicitacoes(self, request):
        usuario = request.user
        alimentacoes_normais = GrupoInclusaoAlimentacaoNormal.get_solicitacoes_rascunho(usuario)
        page = self.paginate_queryset(alimentacoes_normais)
        serializer = serializers.GrupoInclusaoAlimentacaoNormalSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False,
            url_path=f'{constants.PEDIDOS_CODAE}/{constants.FILTRO_PADRAO_PEDIDOS}')
    def solicitacoes_codae(self, request, filtro_aplicado=constants.SEM_FILTRO):
        # TODO: colocar regras de codae CODAE aqui...
        usuario = request.user
        codae = usuario.vinculo_atual.instituicao
        inclusoes_continuas = codae.grupos_inclusoes_alimentacao_normal_das_minhas_escolas(
            filtro_aplicado
        )
        page = self.paginate_queryset(inclusoes_continuas)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False,
            url_path=f'{constants.PEDIDOS_TERCEIRIZADA}/{constants.FILTRO_PADRAO_PEDIDOS}')
    def solicitacoes_terceirizada(self, request, filtro_aplicado='sem_filtro'):
        # TODO: colocar regras de terceirizada aqui...
        usuario = request.user
        terceirizada = usuario.vinculo_atual.instituicao
        inclusoes_continuas = terceirizada.grupos_inclusoes_alimentacao_normal_das_minhas_escolas(
            filtro_aplicado
        )
        page = self.paginate_queryset(inclusoes_continuas)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    # TODO rever os demais endpoints. Essa action consolida em uma única pesquisa as pesquisas por prioridade.
    @action(detail=False,
            url_path=f'{constants.PEDIDOS_DRE}/{constants.FILTRO_PADRAO_PEDIDOS}')
    def solicitacoes_diretoria_regional(self, request, filtro_aplicado=constants.SEM_FILTRO):
        usuario = request.user
        diretoria_regional = usuario.vinculo_atual.instituicao
        inclusoes_alimentacao_normal = diretoria_regional.grupos_inclusoes_alimentacao_normal_das_minhas_escolas(
            filtro_aplicado
        )
        page = self.paginate_queryset(inclusoes_alimentacao_normal)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False, url_path='pedidos-autorizados-diretoria-regional')
    def solicitacoes_autorizados_diretoria_regional(self, request):
        usuario = request.user
        diretoria_regional = usuario.vinculo_atual.instituicao
        inclusoes_normais = diretoria_regional.inclusoes_normais_autorizadas
        page = self.paginate_queryset(inclusoes_normais)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False, url_path='pedidos-reprovados-diretoria-regional')
    def solicitacoes_reprovados_diretoria_regional(self, request):
        usuario = request.user
        diretoria_regional = usuario.vinculo_atual.instituicao
        inclusoes_normais = diretoria_regional.inclusoes_normais_reprovadas
        page = self.paginate_queryset(inclusoes_normais)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False, url_path='pedidos-autorizados-codae')
    def solicitacoes_autorizadas_codae(self, request):
        usuario = request.user
        codae = usuario.vinculo_atual.instituicao
        inclusoes_normais = codae.inclusoes_normais_autorizadas
        page = self.paginate_queryset(inclusoes_normais)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False, url_path='pedidos-reprovados-codae')
    def solicitacoes_reprovados_codae(self, request):
        usuario = request.user
        codae = usuario.vinculo_atual.instituicao
        inclusoes_normais = codae.inclusoes_normais_reprovadas
        page = self.paginate_queryset(inclusoes_normais)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False, url_path='pedidos-autorizados-terceirizada')
    def solicitacoes_autorizadas_terceirizada(self, request):
        usuario = request.user
        terceirizada = usuario.vinculo_atual.instituicao
        inclusoes_normais = terceirizada.inclusoes_normais_autorizadas
        page = self.paginate_queryset(inclusoes_normais)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False, url_path='pedidos-reprovados-terceirizada')
    def solicitacoes_reprovados_terceirizada(self, request):
        usuario = request.user
        terceirizada = usuario.vinculo_atual.instituicao
        inclusoes_normais = terceirizada.inclusoes_normais_reprovadas
        page = self.paginate_queryset(inclusoes_normais)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    #
    # IMPLEMENTACAO DO FLUXO
    #

    @action(detail=True, permission_classes=[PodeIniciarInclusaoAlimentacaoContinuaPermission],
            methods=['patch'], url_path=constants.ESCOLA_INICIO_PEDIDO)
    def inicio_de_pedido(self, request, uuid=None):
        grupo_alimentacao_normal = self.get_object()
        try:
            grupo_alimentacao_normal.inicia_fluxo(user=request.user, )
            serializer = self.get_serializer(grupo_alimentacao_normal)
            return Response(serializer.data)
        except InvalidTransitionError as e:
            return Response(dict(detail=f'Erro de transição de estado: {e}'))

    @action(detail=True, permission_classes=[PodeAprovarAlimentacaoContinuaDaEscolaPermission],
            methods=['patch'], url_path=constants.DRE_VALIDA_PEDIDO)
    def diretoria_regional_valida(self, request, uuid=None):
        grupo_alimentacao_normal = self.get_object()
        try:
            grupo_alimentacao_normal.dre_valida(user=request.user, )
            serializer = self.get_serializer(grupo_alimentacao_normal)
            return Response(serializer.data)
        except InvalidTransitionError as e:
            return Response(dict(detail=f'Erro de transição de estado: {e}'))

    @action(detail=True, permission_classes=[PodeAprovarAlimentacaoContinuaDaEscolaPermission],
            methods=['patch'], url_path=constants.DRE_NAO_VALIDA_PEDIDO)
    def diretoria_cancela_pedido(self, request, uuid=None):
        grupo_alimentacao_normal = self.get_object()
        try:
            grupo_alimentacao_normal.dre_nao_valida(user=request.user, )
            serializer = self.get_serializer(grupo_alimentacao_normal)
            return Response(serializer.data)
        except InvalidTransitionError as e:
            return Response(dict(detail=f'Erro de transição de estado: {e}'))

    @action(detail=True, permission_classes=[PodeAprovarAlimentacaoContinuaDaEscolaPermission],
            methods=['patch'], url_path=constants.CODAE_AUTORIZA_PEDIDO)
    def codae_autoriza_pedido(self, request, uuid=None):
        grupo_alimentacao_normal = self.get_object()
        try:
            grupo_alimentacao_normal.codae_autoriza(user=request.user, )
            serializer = self.get_serializer(grupo_alimentacao_normal)
            return Response(serializer.data)
        except InvalidTransitionError as e:
            return Response(dict(detail=f'Erro de transição de estado: {e}'))

    @action(detail=True, permission_classes=[PodeAprovarAlimentacaoContinuaDaEscolaPermission],
            methods=['patch'], url_path=constants.CODAE_NEGA_PEDIDO)
    def codae_cancela_pedido(self, request, uuid=None):
        grupo_alimentacao_normal = self.get_object()
        try:
            grupo_alimentacao_normal.codae_nega(user=request.user, )
            serializer = self.get_serializer(grupo_alimentacao_normal)
            return Response(serializer.data)
        except InvalidTransitionError as e:
            return Response(dict(detail=f'Erro de transição de estado: {e}'))

    @action(detail=True, permission_classes=[PodeAprovarAlimentacaoContinuaDaEscolaPermission],
            methods=['patch'], url_path=constants.TERCEIRIZADA_TOMOU_CIENCIA)
    def terceirizada_toma_ciencia(self, request, uuid=None):
        grupo_alimentacao_normal = self.get_object()
        try:
            grupo_alimentacao_normal.terceirizada_toma_ciencia(user=request.user, )
            serializer = self.get_serializer(grupo_alimentacao_normal)
            return Response(serializer.data)
        except InvalidTransitionError as e:
            return Response(dict(detail=f'Erro de transição de estado: {e}'))

    @action(detail=True, permission_classes=[PodeAprovarAlimentacaoContinuaDaEscolaPermission],
            methods=['patch'], url_path=constants.ESCOLA_CANCELA)
    def escola_cancela_pedido(self, request, uuid=None):
        justificativa = request.data.get('justificativa', '')
        grupo_alimentacao_normal = self.get_object()
        try:
            grupo_alimentacao_normal.cancelar_pedido(user=request.user, justificativa=justificativa)
            serializer = self.get_serializer(grupo_alimentacao_normal)
            return Response(serializer.data)
        except InvalidTransitionError as e:
            return Response(dict(detail=f'Erro de transição de estado: {e}'), status=HTTP_400_BAD_REQUEST)


class InclusaoAlimentacaoContinuaViewSet(ModelViewSet):
    lookup_field = 'uuid'
    queryset = InclusaoAlimentacaoContinua.objects.all()
    serializer_class = serializers.InclusaoAlimentacaoContinuaSerializer

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return serializers_create.InclusaoAlimentacaoContinuaCreationSerializer
        return serializers.InclusaoAlimentacaoContinuaSerializer

    @action(detail=False, url_path=constants.SOLICITACOES_DO_USUARIO)
    def minhas_solicitacoes(self, request):
        usuario = request.user
        inclusoes_continuas = InclusaoAlimentacaoContinua.get_solicitacoes_rascunho(usuario)
        page = self.paginate_queryset(inclusoes_continuas)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False,
            url_path=f'{constants.PEDIDOS_CODAE}/{constants.FILTRO_PADRAO_PEDIDOS}')
    def solicitacoes_codae(self, request, filtro_aplicado=constants.SEM_FILTRO):
        # TODO: colocar regras de codae CODAE aqui...
        usuario = request.user
        codae = usuario.vinculo_atual.instituicao
        inclusoes_continuas = codae.inclusoes_alimentacao_continua_das_minhas_escolas(
            filtro_aplicado
        )
        page = self.paginate_queryset(inclusoes_continuas)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False,
            url_path=f'{constants.PEDIDOS_TERCEIRIZADA}/{constants.FILTRO_PADRAO_PEDIDOS}')
    def solicitacoes_terceirizada(self, request, filtro_aplicado=constants.SEM_FILTRO):
        # TODO: colocar regras de terceirizada aqui...
        usuario = request.user
        terceirizada = usuario.vinculo_atual.instituicao
        inclusoes_continuas = terceirizada.inclusoes_alimentacao_continua_das_minhas_escolas(
            filtro_aplicado
        )
        page = self.paginate_queryset(inclusoes_continuas)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False,
            url_path=f'{constants.PEDIDOS_DRE}/{constants.FILTRO_PADRAO_PEDIDOS}')
    def solicitacoes_diretoria_regional(self, request, filtro_aplicado=constants.SEM_FILTRO):
        usuario = request.user
        diretoria_regional = usuario.vinculo_atual.instituicao
        inclusoes_alimentacao_continua = diretoria_regional.inclusoes_alimentacao_continua_das_minhas_escolas(
            filtro_aplicado
        )
        page = self.paginate_queryset(inclusoes_alimentacao_continua)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False, url_path='pedidos-autorizados-diretoria-regional')
    def solicitacoes_autorizadas_diretoria_regional(self, request):
        usuario = request.user
        diretoria_regional = usuario.vinculo_atual.instituicao
        inclusoes_continuas = diretoria_regional.inclusoes_continuas_autorizadas
        page = self.paginate_queryset(inclusoes_continuas)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False, url_path='pedidos-reprovados-diretoria-regional')
    def solicitacoes_reprovados_diretoria_regional(self, request):
        usuario = request.user
        diretoria_regional = usuario.vinculo_atual.instituicao
        inclusoes_continuas = diretoria_regional.inclusoes_continuas_reprovadas
        page = self.paginate_queryset(inclusoes_continuas)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False, url_path='pedidos-autorizados-codae')
    def solicitacoes_autorizadas_codae(self, request):
        usuario = request.user
        codae = usuario.vinculo_atual.instituicao
        inclusoes_continuas = codae.inclusoes_continuas_autorizadas
        page = self.paginate_queryset(inclusoes_continuas)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False, url_path='pedidos-reprovados-codae')
    def solicitacoes_reprovados_codae(self, request):
        usuario = request.user
        codae = usuario.vinculo_atual.instituicao
        inclusoes_continuas = codae.inclusoes_continuas_reprovadas
        page = self.paginate_queryset(inclusoes_continuas)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False, url_path='pedidos-autorizados-terceirizada')
    def solicitacoes_autorizadas_terceirizada(self, request):
        usuario = request.user
        terceirizada = usuario.vinculo_atual.instituicao
        inclusoes_continuas = terceirizada.inclusoes_continuas_autorizadas
        page = self.paginate_queryset(inclusoes_continuas)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False, url_path='pedidos-reprovados-terceirizada')
    def solicitacoes_reprovados_terceirizada(self, request):
        usuario = request.user
        terceirizada = usuario.vinculo_atual.instituicao
        inclusoes_continuas = terceirizada.inclusoes_continuas_reprovadas
        page = self.paginate_queryset(inclusoes_continuas)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    #
    # IMPLEMENTACAO DO FLUXO
    #

    @action(detail=True, permission_classes=[PodeIniciarInclusaoAlimentacaoContinuaPermission],
            methods=['patch'], url_path=constants.ESCOLA_INICIO_PEDIDO)
    def inicio_de_pedido(self, request, uuid=None):
        inclusao_alimentacao_continua = self.get_object()
        try:
            inclusao_alimentacao_continua.inicia_fluxo(user=request.user, )
            serializer = self.get_serializer(inclusao_alimentacao_continua)
            return Response(serializer.data)
        except InvalidTransitionError as e:
            return Response(dict(detail=f'Erro de transição de estado: {e}'))

    @action(detail=True, permission_classes=[PodeAprovarAlimentacaoContinuaDaEscolaPermission],
            methods=['patch'], url_path=constants.DRE_VALIDA_PEDIDO)
    def diretoria_regional_valida(self, request, uuid=None):
        inclusao_alimentacao_continua = self.get_object()
        try:
            inclusao_alimentacao_continua.dre_valida(user=request.user, )
            serializer = self.get_serializer(inclusao_alimentacao_continua)
            return Response(serializer.data)
        except InvalidTransitionError as e:
            return Response(dict(detail=f'Erro de transição de estado: {e}'))

    @action(detail=True, permission_classes=[PodeAprovarAlimentacaoContinuaDaEscolaPermission],
            methods=['patch'], url_path=constants.CODAE_NEGA_PEDIDO)
    def codae_cancela_pedido(self, request, uuid=None):
        inclusao_alimentacao_continua = self.get_object()
        try:
            inclusao_alimentacao_continua.codae_nega(user=request.user, )
            serializer = self.get_serializer(inclusao_alimentacao_continua)
            return Response(serializer.data)
        except InvalidTransitionError as e:
            return Response(dict(detail=f'Erro de transição de estado: {e}'))

    @action(detail=True, permission_classes=[PodeAprovarAlimentacaoContinuaDaEscolaPermission],
            methods=['patch'], url_path=constants.DRE_NAO_VALIDA_PEDIDO)
    def diretoria_regional_cancela_pedido(self, request, uuid=None):
        inclusao_alimentacao_continua = self.get_object()
        try:
            inclusao_alimentacao_continua.dre_nao_valida(user=request.user, )
            serializer = self.get_serializer(inclusao_alimentacao_continua)
            return Response(serializer.data)
        except InvalidTransitionError as e:
            return Response(dict(detail=f'Erro de transição de estado: {e}'))

    @action(detail=True, permission_classes=[PodeAprovarAlimentacaoContinuaDaEscolaPermission],
            methods=['patch'], url_path=constants.CODAE_AUTORIZA_PEDIDO)
    def codae_autoriza_pedido(self, request, uuid=None):
        inclusao_alimentacao_continua = self.get_object()
        try:
            inclusao_alimentacao_continua.codae_autoriza(user=request.user, )
            serializer = self.get_serializer(inclusao_alimentacao_continua)
            return Response(serializer.data)
        except InvalidTransitionError as e:
            return Response(dict(detail=f'Erro de transição de estado: {e}'))

    @action(detail=True, permission_classes=[PodeAprovarAlimentacaoContinuaDaEscolaPermission],
            methods=['patch'], url_path=constants.TERCEIRIZADA_TOMOU_CIENCIA)
    def terceirizada_toma_ciencia(self, request, uuid=None):
        inclusao_alimentacao_continua = self.get_object()
        try:
            inclusao_alimentacao_continua.terceirizada_toma_ciencia(user=request.user, )
            serializer = self.get_serializer(inclusao_alimentacao_continua)
            return Response(serializer.data)
        except InvalidTransitionError as e:
            return Response(dict(detail=f'Erro de transição de estado: {e}'))

    @action(detail=True, permission_classes=[PodeAprovarAlimentacaoContinuaDaEscolaPermission],
            methods=['patch'], url_path=constants.ESCOLA_CANCELA)
    def escola_cancela_pedido(self, request, uuid=None):
        inclusao_alimentacao_continua = self.get_object()
        justificativa = request.data.get('justificativa', '')
        try:
            inclusao_alimentacao_continua.cancelar_pedido(user=request.user, justificativa=justificativa)
            serializer = self.get_serializer(inclusao_alimentacao_continua)
            return Response(serializer.data)
        except InvalidTransitionError as e:
            return Response(dict(detail=f'Erro de transição de estado: {e}'), status=HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        inclusao_alimentacao_continua = self.get_object()
        if inclusao_alimentacao_continua.pode_excluir:
            return super().destroy(request, *args, **kwargs)
