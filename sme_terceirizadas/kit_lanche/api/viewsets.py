from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from xworkflows import InvalidTransitionError

from ...dados_comuns import constants
from .. import models
from ..api.validators import nao_deve_ter_mais_solicitacoes_que_alunos
from ..models import SolicitacaoKitLancheAvulsa, SolicitacaoKitLancheUnificada
from .permissions import PodeIniciarSolicitacaoKitLancheAvulsaPermission, PodeIniciarSolicitacaoUnificadaPermission
from .serializers import serializers, serializers_create


class KitLancheViewSet(ReadOnlyModelViewSet):
    lookup_field = 'uuid'
    queryset = models.KitLanche.objects.all()
    serializer_class = serializers.KitLancheSerializer


class SolicitacaoKitLancheAvulsaViewSet(ModelViewSet):
    lookup_field = 'uuid'
    queryset = SolicitacaoKitLancheAvulsa.objects.all()
    serializer_class = serializers.SolicitacaoKitLancheAvulsaSerializer

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return serializers_create.SolicitacaoKitLancheAvulsaCreationSerializer
        return serializers.SolicitacaoKitLancheAvulsaSerializer

    @action(detail=False,
            url_path=f'{constants.PEDIDOS_DRE}/{constants.FILTRO_PADRAO_PEDIDOS}')
    def pedidos_diretoria_regional(self, request, filtro_aplicado='sem_filtro'):
        usuario = request.user
        diretoria_regional = usuario.vinculo_atual.instituicao
        kit_lanches_avulso = diretoria_regional.solicitacoes_kit_lanche_das_minhas_escolas_a_validar(
            filtro_aplicado
        )
        page = self.paginate_queryset(kit_lanches_avulso)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False, url_path='pedidos-autorizados-diretoria-regional')
    def pedidos_autorizados_diretoria_regional(self, request):
        usuario = request.user
        diretoria_regional = usuario.vinculo_atual.instituicao
        kit_lanche = diretoria_regional.solicitacao_kit_lanche_avulsa_autorizadas
        page = self.paginate_queryset(kit_lanche)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False, url_path='pedidos-reprovados-diretoria-regional')
    def pedidos_reprovados_diretoria_regional(self, request):
        usuario = request.user
        diretoria_regional = usuario.vinculo_atual.instituicao
        kit_lanche = diretoria_regional.solicitacao_kit_lanche_avulsa_reprovados
        page = self.paginate_queryset(kit_lanche)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False, url_path='pedidos-autorizados-codae')
    def pedidos_autorizados_codae(self, request):
        usuario = request.user
        codae = usuario.vinculo_atual.instituicao
        kit_lanche = codae.solicitacao_kit_lanche_avulsa_autorizadas
        page = self.paginate_queryset(kit_lanche)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False, url_path='pedidos-reprovados-codae')
    def pedidos_reprovados_codae(self, request):
        usuario = request.user
        codae = usuario.vinculo_atual.instituicao
        kit_lanche = codae.solicitacao_kit_lanche_avulsa_reprovadas
        page = self.paginate_queryset(kit_lanche)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False, url_path='pedidos-autorizados-terceirizadas')
    def pedidos_autorizados_terceirizadas(self, request):
        usuario = request.user
        terceirizadas = usuario.vinculo_atual.instituicao
        kit_lanche = terceirizadas.solicitacao_kit_lanche_avulsa_autorizadas
        page = self.paginate_queryset(kit_lanche)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False,
            url_path=f'{constants.PEDIDOS_CODAE}/{constants.FILTRO_PADRAO_PEDIDOS}')
    def pedidos_codae(self, request, filtro_aplicado='sem_filtro'):
        usuario = request.user
        codae = usuario.vinculo_atual.instituicao
        kit_lanches_avulso = codae.solicitacoes_kit_lanche_das_minhas_escolas_a_validar(
            filtro_aplicado
        )
        page = self.paginate_queryset(kit_lanches_avulso)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False,
            url_path=f'{constants.PEDIDOS_TERCEIRIZADA}/{constants.FILTRO_PADRAO_PEDIDOS}')
    def pedidos_terceirizadas(self, request, filtro_aplicado='sem_filtro'):
        usuario = request.user
        terceirizadas = usuario.vinculo_atual.instituicao
        kit_lanches_avulso = terceirizadas.solicitacoes_kit_lanche_das_minhas_escolas_a_validar(
            filtro_aplicado
        )
        page = self.paginate_queryset(kit_lanches_avulso)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    # TODO: com as permissoes feitas, somente uma pessoa com permissao dentro da escola poder pedir
    @action(detail=False, url_path=constants.SOLICITACOES_DO_USUARIO)
    def minhas_solicitacoes(self, request):
        usuario = request.user
        solicitacoes_unificadas = SolicitacaoKitLancheAvulsa.objects.filter(
            criado_por=usuario,
            status=SolicitacaoKitLancheAvulsa.workflow_class.RASCUNHO
        )
        page = self.paginate_queryset(solicitacoes_unificadas)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    #
    # IMPLEMENTAÇÃO DO FLUXO (PARTINDO DA ESCOLA)
    #

    @action(detail=True, permission_classes=[PodeIniciarSolicitacaoKitLancheAvulsaPermission],
            methods=['patch'], url_path=constants.ESCOLA_INICIO_PEDIDO)
    def inicio_de_pedido(self, request, uuid=None):
        solicitacao_kit_lanche_avulsa = self.get_object()
        try:
            nao_deve_ter_mais_solicitacoes_que_alunos(solicitacao_kit_lanche_avulsa)

            solicitacao_kit_lanche_avulsa.inicia_fluxo(user=request.user, )
            serializer = self.get_serializer(solicitacao_kit_lanche_avulsa)
            return Response(serializer.data)
        except InvalidTransitionError as e:
            return Response(dict(detail=f'Erro de transição de estado: {e}'), status=HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response(dict(detail=f'{str(e.detail[0])}'), status=HTTP_400_BAD_REQUEST)

    @action(detail=True, permission_classes=[PodeIniciarSolicitacaoKitLancheAvulsaPermission],
            methods=['patch'], url_path=constants.DRE_VALIDA_PEDIDO)
    def diretoria_regional_valida_pedido(self, request, uuid=None):
        solicitacao_kit_lanche_avulsa = self.get_object()
        try:
            solicitacao_kit_lanche_avulsa.dre_valida(user=request.user, )
            serializer = self.get_serializer(solicitacao_kit_lanche_avulsa)
            return Response(serializer.data, status=HTTP_200_OK)
        except InvalidTransitionError as e:
            return Response(dict(detail=f'Erro de transição de estado: {e}'), status=HTTP_400_BAD_REQUEST)

    @action(detail=True, permission_classes=[PodeIniciarSolicitacaoKitLancheAvulsaPermission],
            methods=['patch'], url_path=constants.DRE_NAO_VALIDA_PEDIDO)
    def diretoria_regional_nao_valida(self, request, uuid=None):
        solicitacao_kit_lanche_avulsa = self.get_object()
        justificativa = request.data.get('justificativa', '')
        try:
            solicitacao_kit_lanche_avulsa.dre_nao_valida(user=request.user, justificativa=justificativa)
            serializer = self.get_serializer(solicitacao_kit_lanche_avulsa)
            return Response(serializer.data)
        except InvalidTransitionError as e:
            return Response(dict(detail=f'Erro de transição de estado: {e}'), status=HTTP_400_BAD_REQUEST)

    @action(detail=True, permission_classes=[PodeIniciarSolicitacaoKitLancheAvulsaPermission],
            methods=['patch'], url_path=constants.CODAE_QUESTIONA_PEDIDO)
    def codae_questiona_pedido(self, request, uuid=None):
        solicitacao_kit_lanche_avulsa = self.get_object()
        observacao_questionamento_codae = request.data.get('observacao_questionamento_codae', '')
        try:
            solicitacao_kit_lanche_avulsa.codae_questiona(
                user=request.user,
                justificativa=observacao_questionamento_codae
            )
            serializer = self.get_serializer(solicitacao_kit_lanche_avulsa)
            return Response(serializer.data)
        except InvalidTransitionError as e:
            return Response(dict(detail=f'Erro de transição de estado: {e}'), status=HTTP_400_BAD_REQUEST)

    @action(detail=True, permission_classes=[PodeIniciarSolicitacaoKitLancheAvulsaPermission],
            methods=['patch'], url_path=constants.CODAE_AUTORIZA_PEDIDO)
    def codae_autoriza_pedido(self, request, uuid=None):
        solicitacao_kit_lanche_avulsa = self.get_object()
        try:
            if solicitacao_kit_lanche_avulsa.status == solicitacao_kit_lanche_avulsa.workflow_class.DRE_VALIDADO:
                solicitacao_kit_lanche_avulsa.codae_autoriza(user=request.user)
            else:
                solicitacao_kit_lanche_avulsa.codae_autoriza_questionamento(user=request.user)
            serializer = self.get_serializer(solicitacao_kit_lanche_avulsa)
            return Response(serializer.data)
        except InvalidTransitionError as e:
            return Response(dict(detail=f'Erro de transição de estado: {e}'), status=HTTP_400_BAD_REQUEST)

    @action(detail=True, permission_classes=[PodeIniciarSolicitacaoKitLancheAvulsaPermission],
            methods=['patch'], url_path=constants.CODAE_NEGA_PEDIDO)
    def codae_nega_pedido(self, request, uuid=None):
        solicitacao_kit_lanche_avulsa = self.get_object()
        justificativa = request.data.get('justificativa', '')
        try:
            if solicitacao_kit_lanche_avulsa.status == solicitacao_kit_lanche_avulsa.workflow_class.DRE_VALIDADO:
                solicitacao_kit_lanche_avulsa.codae_nega(user=request.user, justificativa=justificativa)
            else:
                solicitacao_kit_lanche_avulsa.codae_nega_questionamento(user=request.user, justificativa=justificativa)
            serializer = self.get_serializer(solicitacao_kit_lanche_avulsa)
            return Response(serializer.data)
        except InvalidTransitionError as e:
            return Response(dict(detail=f'Erro de transição de estado: {e}'), status=HTTP_400_BAD_REQUEST)

    @action(detail=True, permission_classes=[PodeIniciarSolicitacaoKitLancheAvulsaPermission],
            methods=['patch'], url_path=constants.TERCEIRIZADA_RESPONDE_QUESTIONAMENTO)
    def terceirizada_responde_questionamento(self, request, uuid=None):
        solicitacao_kit_lanche_avulsa = self.get_object()
        justificativa = request.data.get('justificativa', '')
        resposta_sim_nao = request.data.get('resposta_sim_nao', False)
        try:
            solicitacao_kit_lanche_avulsa.terceirizada_responde_questionamento(user=request.user,
                                                                               justificativa=justificativa,
                                                                               resposta_sim_nao=resposta_sim_nao)
            serializer = self.get_serializer(solicitacao_kit_lanche_avulsa)
            return Response(serializer.data)
        except InvalidTransitionError as e:
            return Response(dict(detail=f'Erro de transição de estado: {e}'), status=HTTP_400_BAD_REQUEST)

    @action(detail=True, permission_classes=[PodeIniciarSolicitacaoKitLancheAvulsaPermission],
            methods=['patch'], url_path=constants.TERCEIRIZADA_TOMOU_CIENCIA)
    def terceirizada_toma_ciencia(self, request, uuid=None):
        solicitacao_kit_lanche_avulsa = self.get_object()
        try:
            solicitacao_kit_lanche_avulsa.terceirizada_toma_ciencia(user=request.user, )
            serializer = self.get_serializer(solicitacao_kit_lanche_avulsa)
            return Response(serializer.data)
        except InvalidTransitionError as e:
            return Response(dict(detail=f'Erro de transição de estado: {e}'), status=HTTP_400_BAD_REQUEST)

    @action(detail=True, permission_classes=[PodeIniciarSolicitacaoKitLancheAvulsaPermission],
            methods=['patch'], url_path=constants.ESCOLA_CANCELA)
    def escola_cancela_pedido(self, request, uuid=None):
        justificativa = request.data.get('justificativa', '')
        solicitacao_kit_lanche_avulsa = self.get_object()
        try:
            solicitacao_kit_lanche_avulsa.cancelar_pedido(user=request.user,
                                                          justificativa=justificativa)
            serializer = self.get_serializer(solicitacao_kit_lanche_avulsa)
            return Response(serializer.data)
        except InvalidTransitionError as e:
            return Response(dict(detail=f'Erro de transição de estado: {e}'), status=HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        solicitacao_kit_lanche_avulsa = self.get_object()
        if solicitacao_kit_lanche_avulsa.pode_excluir:
            return super().destroy(request, *args, **kwargs)


class SolicitacaoKitLancheUnificadaViewSet(ModelViewSet):
    lookup_field = 'uuid'
    queryset = SolicitacaoKitLancheUnificada.objects.all()
    serializer_class = serializers.SolicitacaoKitLancheUnificadaSerializer

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return serializers_create.SolicitacaoKitLancheUnificadaCreationSerializer
        return serializers.SolicitacaoKitLancheUnificadaSerializer

    @action(detail=False,
            url_path=f'{constants.PEDIDOS_CODAE}/{constants.FILTRO_PADRAO_PEDIDOS}')
    def pedidos_codae(self, request, filtro_aplicado=constants.SEM_FILTRO):
        # TODO: colocar regras de codae CODAE aqui...
        usuario = request.user
        codae = usuario.vinculo_atual.instituicao
        solicitacoes_unificadas = codae.solicitacoes_unificadas(
            filtro_aplicado
        )
        page = self.paginate_queryset(solicitacoes_unificadas)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False,
            url_path=f'{constants.PEDIDOS_TERCEIRIZADA}/{constants.FILTRO_PADRAO_PEDIDOS}')
    def pedidos_terceirizada(self, request, filtro_aplicado=constants.SEM_FILTRO):
        # TODO: colocar regras de Terceirizada aqui...
        usuario = request.user
        terceirizada = usuario.vinculo_atual.instituicao
        solicitacoes_unificadas = terceirizada.solicitacoes_unificadas_das_minhas_escolas(
            filtro_aplicado
        )
        page = self.paginate_queryset(solicitacoes_unificadas)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False, url_path='pedidos-autorizados-codae')
    def pedidos_autorizados_codae(self, request):
        usuario = request.user
        codae = usuario.vinculo_atual.instituicao
        kit_lanche = codae.solicitacoes_unificadas_autorizadas
        page = self.paginate_queryset(kit_lanche)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False, url_path='pedidos-autorizados-terceirizada')
    def pedidos_autorizados_terceirizada(self, request):
        usuario = request.user
        terceirizada = usuario.vinculo_atual.instituicao
        kit_lanche = terceirizada.solicitacoes_unificadas_autorizadas
        page = self.paginate_queryset(kit_lanche)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False, url_path=constants.SOLICITACOES_DO_USUARIO)
    def minhas_solicitacoes(self, request):
        usuario = request.user
        solicitacoes_unificadas = SolicitacaoKitLancheUnificada.get_pedidos_rascunho(usuario)
        page = self.paginate_queryset(solicitacoes_unificadas)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    #
    # IMPLEMENTAÇÃO DO FLUXO (PARTINDO DA DRE)
    #

    @action(detail=True, url_path=constants.DRE_INICIO_PEDIDO,
            permission_classes=[PodeIniciarSolicitacaoUnificadaPermission], methods=['patch'])
    def inicio_de_pedido(self, request, uuid=None):
        solicitacao_unificada = self.get_object()
        try:
            solicitacoes_unificadas = solicitacao_unificada.dividir_por_lote()
            for solicitacao_unificada in solicitacoes_unificadas:
                solicitacao_unificada.inicia_fluxo(user=request.user)
            serializer = self.get_serializer(solicitacoes_unificadas, many=True)
            return Response(serializer.data)
        except InvalidTransitionError as e:
            return Response(dict(detail=f'Erro de transição de estado: {e}'), status=HTTP_400_BAD_REQUEST)

    @action(detail=True, url_path=constants.CODAE_AUTORIZA_PEDIDO,
            permission_classes=[PodeIniciarSolicitacaoUnificadaPermission], methods=['patch'])
    def codae_autoriza(self, request, uuid=None):
        solicitacao_unificada = self.get_object()
        try:
            solicitacao_unificada.codae_autoriza(user=request.user, )
            serializer = self.get_serializer(solicitacao_unificada)
            return Response(serializer.data)
        except InvalidTransitionError as e:
            return Response(dict(detail=f'Erro de transição de estado: {e}'), status=HTTP_400_BAD_REQUEST)

    @action(detail=True, url_path=constants.CODAE_NEGA_PEDIDO,
            permission_classes=[PodeIniciarSolicitacaoUnificadaPermission], methods=['patch'])
    def codae_nega_pedido(self, request, uuid=None):
        solicitacao_unificada = self.get_object()
        justificativa = request.data.get('justificativa', '')
        try:
            solicitacao_unificada.codae_nega(user=request.user, justificativa=justificativa)
            serializer = self.get_serializer(solicitacao_unificada)
            return Response(serializer.data)
        except InvalidTransitionError as e:
            return Response(dict(detail=f'Erro de transição de estado: {e}'), status=HTTP_400_BAD_REQUEST)

    @action(detail=True, url_path=constants.TERCEIRIZADA_TOMOU_CIENCIA,
            permission_classes=[PodeIniciarSolicitacaoUnificadaPermission], methods=['patch'])
    def terceirizada_toma_ciencia(self, request, uuid=None):
        solicitacao_unificada = self.get_object()
        try:
            solicitacao_unificada.terceirizada_toma_ciencia(user=request.user, )
            serializer = self.get_serializer(solicitacao_unificada)
            return Response(serializer.data)
        except InvalidTransitionError as e:
            return Response(dict(detail=f'Erro de transição de estado: {e}'), status=HTTP_400_BAD_REQUEST)

    @action(detail=True, url_path=constants.DRE_CANCELA,
            permission_classes=[PodeIniciarSolicitacaoUnificadaPermission], methods=['patch'])
    def diretoria_regional_cancela(self, request, uuid=None):
        justificativa = request.data.get('justificativa', '')
        solicitacao_unificada = self.get_object()
        try:
            solicitacao_unificada.cancelar_pedido(user=request.user, justificativa=justificativa)
            serializer = self.get_serializer(solicitacao_unificada)
            return Response(serializer.data)
        except InvalidTransitionError as e:
            return Response(dict(detail=f'Erro de transição de estado: {e}'), status=HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        solicitacao_unificada = self.get_object()
        if solicitacao_unificada.pode_excluir:
            return super().destroy(request, *args, **kwargs)
