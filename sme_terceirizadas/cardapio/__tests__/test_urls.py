from freezegun import freeze_time
from rest_framework import status

from ...dados_comuns import constants
from ...dados_comuns.fluxo_status import InformativoPartindoDaEscolaWorkflow, PedidoAPartirDaEscolaWorkflow

ENRPOINT_INVERSOES = 'inversoes-dia-cardapio'
ENDPOINT_SUSPENSOES = 'grupos-suspensoes-alimentacao'
ENDPOINT_ALTERACAO_CARD = 'alteracoes-cardapio'
ENDPOINT_VINCULOS_ALIMENTACAO = 'vinculos-tipo-alimentacao-u-e-periodo-escolar'


def test_url_endpoint_solicitacoes_inversao_inicio_fluxo(client_autenticado, inversao_dia_cardapio):
    assert str(inversao_dia_cardapio.status) == PedidoAPartirDaEscolaWorkflow.RASCUNHO
    response = client_autenticado.patch(
        f'/{ENRPOINT_INVERSOES}/{inversao_dia_cardapio.uuid}/{constants.ESCOLA_INICIO_PEDIDO}/'
    )
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json['status'] == PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR
    assert str(json['uuid']) == str(inversao_dia_cardapio.uuid)


def test_url_endpoint_solicitacoes_inversao_inicio_fluxo_error(client_autenticado, inversao_dia_cardapio_dre_validar):
    assert str(inversao_dia_cardapio_dre_validar.status) == PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR
    response = client_autenticado.patch(
        f'/{ENRPOINT_INVERSOES}/{inversao_dia_cardapio_dre_validar.uuid}/{constants.ESCOLA_INICIO_PEDIDO}/'
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'detail': "Erro de transição de estado: Transition 'inicia_fluxo' isn't available from state 'DRE_A_VALIDAR'."}


def test_url_endpoint_solicitacoes_inversao_dre_valida(client_autenticado, inversao_dia_cardapio_dre_validar):
    assert str(inversao_dia_cardapio_dre_validar.status) == PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR
    response = client_autenticado.patch(
        f'/{ENRPOINT_INVERSOES}/{inversao_dia_cardapio_dre_validar.uuid}/{constants.DRE_VALIDA_PEDIDO}/'
    )
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json['status'] == PedidoAPartirDaEscolaWorkflow.DRE_VALIDADO
    assert str(json['uuid']) == str(inversao_dia_cardapio_dre_validar.uuid)


def test_url_endpoint_solicitacoes_inversao_dre_valida_error(client_autenticado, inversao_dia_cardapio_dre_validado):
    assert str(inversao_dia_cardapio_dre_validado.status) == PedidoAPartirDaEscolaWorkflow.DRE_VALIDADO
    response = client_autenticado.patch(
        f'/{ENRPOINT_INVERSOES}/{inversao_dia_cardapio_dre_validado.uuid}/{constants.DRE_VALIDA_PEDIDO}/'
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'detail': "Erro de transição de estado: Transition 'dre_valida' isn't available from state 'DRE_VALIDADO'."}


def test_url_endpoint_solicitacoes_inversao_codae_autoriza(client_autenticado, inversao_dia_cardapio_dre_validado):
    assert str(inversao_dia_cardapio_dre_validado.status) == PedidoAPartirDaEscolaWorkflow.DRE_VALIDADO
    response = client_autenticado.patch(
        f'/{ENRPOINT_INVERSOES}/{inversao_dia_cardapio_dre_validado.uuid}/{constants.CODAE_AUTORIZA_PEDIDO}/'
    )
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json['status'] == PedidoAPartirDaEscolaWorkflow.CODAE_AUTORIZADO
    assert str(json['uuid']) == str(inversao_dia_cardapio_dre_validado.uuid)


def test_url_endpoint_solicitacoes_inversao_codae_autoriza_error(client_autenticado, inversao_dia_cardapio_dre_validar):
    assert str(inversao_dia_cardapio_dre_validar.status) == PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR
    response = client_autenticado.patch(
        f'/{ENRPOINT_INVERSOES}/{inversao_dia_cardapio_dre_validar.uuid}/{constants.CODAE_AUTORIZA_PEDIDO}/'
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'detail': "Erro de transição de estado: Transition 'codae_autoriza_questionamento' "
                  "isn't available from state 'DRE_A_VALIDAR'."}


def test_url_endpoint_solicitacoes_inversao_codae_nega(client_autenticado, inversao_dia_cardapio_dre_validado):
    assert str(inversao_dia_cardapio_dre_validado.status) == PedidoAPartirDaEscolaWorkflow.DRE_VALIDADO
    response = client_autenticado.patch(
        f'/{ENRPOINT_INVERSOES}/{inversao_dia_cardapio_dre_validado.uuid}/{constants.CODAE_NEGA_PEDIDO}/'
    )
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json['status'] == PedidoAPartirDaEscolaWorkflow.CODAE_NEGOU_PEDIDO
    assert str(json['uuid']) == str(inversao_dia_cardapio_dre_validado.uuid)


def test_url_endpoint_solicitacoes_inversao_codae_nega_error(client_autenticado, inversao_dia_cardapio_dre_validar):
    assert str(inversao_dia_cardapio_dre_validar.status) == PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR
    response = client_autenticado.patch(
        f'/{ENRPOINT_INVERSOES}/{inversao_dia_cardapio_dre_validar.uuid}/{constants.CODAE_NEGA_PEDIDO}/'
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'detail': "Erro de transição de estado: Transition 'codae_nega_questionamento'"
                  " isn't available from state 'DRE_A_VALIDAR'."}


def test_url_endpoint_solicitacoes_inversao_terceirizada_ciencia(client_autenticado,
                                                                 inversao_dia_cardapio_codae_autorizado):
    assert str(inversao_dia_cardapio_codae_autorizado.status) == PedidoAPartirDaEscolaWorkflow.CODAE_AUTORIZADO
    response = client_autenticado.patch(
        f'/{ENRPOINT_INVERSOES}/{inversao_dia_cardapio_codae_autorizado.uuid}/{constants.TERCEIRIZADA_TOMOU_CIENCIA}/'
    )
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json['status'] == PedidoAPartirDaEscolaWorkflow.TERCEIRIZADA_TOMOU_CIENCIA
    assert str(json['uuid']) == str(inversao_dia_cardapio_codae_autorizado.uuid)


def test_url_endpoint_solicitacoes_inversao_terceirizada_ciencia_error(client_autenticado,
                                                                       inversao_dia_cardapio_dre_validado):
    assert str(inversao_dia_cardapio_dre_validado.status) == PedidoAPartirDaEscolaWorkflow.DRE_VALIDADO
    response = client_autenticado.patch(
        f'/{ENRPOINT_INVERSOES}/{inversao_dia_cardapio_dre_validado.uuid}/{constants.TERCEIRIZADA_TOMOU_CIENCIA}/'
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'detail': "Erro de transição de estado: Transition 'terceirizada_toma_ciencia' "
                  "isn't available from state 'DRE_VALIDADO'."}


@freeze_time('2019-10-11')
def test_url_endpoint_solicitacoes_inversao_escola_cancela(client_autenticado,
                                                           inversao_dia_cardapio_codae_autorizado):
    assert str(inversao_dia_cardapio_codae_autorizado.status) == PedidoAPartirDaEscolaWorkflow.CODAE_AUTORIZADO
    response = client_autenticado.patch(
        f'/{ENRPOINT_INVERSOES}/{inversao_dia_cardapio_codae_autorizado.uuid}/{constants.ESCOLA_CANCELA}/'
    )
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json['status'] == PedidoAPartirDaEscolaWorkflow.ESCOLA_CANCELOU
    assert str(json['uuid']) == str(inversao_dia_cardapio_codae_autorizado.uuid)


@freeze_time('2019-12-31')
def test_url_endpoint_solicitacoes_inversao_escola_cancela_error(client_autenticado,
                                                                 inversao_dia_cardapio_codae_autorizado):
    assert str(inversao_dia_cardapio_codae_autorizado.status) == PedidoAPartirDaEscolaWorkflow.CODAE_AUTORIZADO
    response = client_autenticado.patch(
        f'/{ENRPOINT_INVERSOES}/{inversao_dia_cardapio_codae_autorizado.uuid}/{constants.ESCOLA_CANCELA}/'
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'detail': 'Erro de transição de estado: Só pode cancelar com no mínimo 2 dia(s) de antecedência'}


def test_url_endpoint_solicitacoes_inversao_codae_questiona_error(client_autenticado,
                                                                  inversao_dia_cardapio_codae_autorizado):
    assert str(inversao_dia_cardapio_codae_autorizado.status) == PedidoAPartirDaEscolaWorkflow.CODAE_AUTORIZADO
    response = client_autenticado.patch(
        f'/{ENRPOINT_INVERSOES}/{inversao_dia_cardapio_codae_autorizado.uuid}/{constants.CODAE_QUESTIONA_PEDIDO}/'
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'detail':
            "Erro de transição de estado: Transition 'codae_questiona' isn't available from state 'CODAE_AUTORIZADO'."
    }


def test_url_endpoint_solicitacoes_inversao_codae_questiona(client_autenticado,
                                                            inversao_dia_cardapio_dre_validado):
    assert str(inversao_dia_cardapio_dre_validado.status) == PedidoAPartirDaEscolaWorkflow.DRE_VALIDADO
    response = client_autenticado.patch(
        f'/{ENRPOINT_INVERSOES}/{inversao_dia_cardapio_dre_validado.uuid}/{constants.CODAE_QUESTIONA_PEDIDO}/'
    )
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json['status'] == PedidoAPartirDaEscolaWorkflow.CODAE_QUESTIONADO
    assert str(json['uuid']) == str(inversao_dia_cardapio_dre_validado.uuid)


#
# Suspensão de alimentação
#


def test_url_endpoint_suspensoes_informa(client_autenticado, grupo_suspensao_alimentacao):
    assert str(grupo_suspensao_alimentacao.status) == InformativoPartindoDaEscolaWorkflow.RASCUNHO
    response = client_autenticado.patch(
        f'/{ENDPOINT_SUSPENSOES}/{grupo_suspensao_alimentacao.uuid}/{constants.ESCOLA_INFORMA_SUSPENSAO}/'
    )
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json['status'] == InformativoPartindoDaEscolaWorkflow.INFORMADO
    assert str(json['uuid']) == str(grupo_suspensao_alimentacao.uuid)


def test_url_endpoint_suspensoes_informa_error(client_autenticado, grupo_suspensao_alimentacao_informado):
    assert str(grupo_suspensao_alimentacao_informado.status) == InformativoPartindoDaEscolaWorkflow.INFORMADO
    response = client_autenticado.patch(
        f'/{ENDPOINT_SUSPENSOES}/{grupo_suspensao_alimentacao_informado.uuid}/{constants.ESCOLA_INFORMA_SUSPENSAO}/'
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': "Erro de transição de estado: Transition 'informa' "
                                         "isn't available from state 'INFORMADO'."}


def test_url_endpoint_suspensoes_terc_ciencia(client_autenticado, grupo_suspensao_alimentacao_informado):
    assert str(grupo_suspensao_alimentacao_informado.status) == InformativoPartindoDaEscolaWorkflow.INFORMADO
    response = client_autenticado.patch(
        f'/{ENDPOINT_SUSPENSOES}/{grupo_suspensao_alimentacao_informado.uuid}/{constants.TERCEIRIZADA_TOMOU_CIENCIA}/'
    )
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json['status'] == InformativoPartindoDaEscolaWorkflow.TERCEIRIZADA_TOMOU_CIENCIA
    assert str(json['uuid']) == str(grupo_suspensao_alimentacao_informado.uuid)


def test_url_endpoint_suspensoes_terc_ciencia_error(client_autenticado, grupo_suspensao_alimentacao):
    assert str(grupo_suspensao_alimentacao.status) == InformativoPartindoDaEscolaWorkflow.RASCUNHO
    response = client_autenticado.patch(
        f'/{ENDPOINT_SUSPENSOES}/{grupo_suspensao_alimentacao.uuid}/{constants.TERCEIRIZADA_TOMOU_CIENCIA}/'
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': "Erro de transição de estado: Transition 'terceirizada_toma_ciencia'"
                                         " isn't available from state 'RASCUNHO'."}


#
# Alteração de cardápio
#

def test_url_endpoint_alt_card_inicio(client_autenticado, alteracao_cardapio):
    assert str(alteracao_cardapio.status) == PedidoAPartirDaEscolaWorkflow.RASCUNHO
    response = client_autenticado.patch(
        f'/{ENDPOINT_ALTERACAO_CARD}/{alteracao_cardapio.uuid}/{constants.ESCOLA_INICIO_PEDIDO}/'
    )

    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json['status'] == PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR
    assert str(json['uuid']) == str(alteracao_cardapio.uuid)


def test_url_endpoint_alt_card_inicio_error(client_autenticado, alteracao_cardapio_dre_validar):
    assert str(alteracao_cardapio_dre_validar.status) == PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR
    response = client_autenticado.patch(
        f'/{ENDPOINT_ALTERACAO_CARD}/{alteracao_cardapio_dre_validar.uuid}/{constants.ESCOLA_INICIO_PEDIDO}/'
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': "Erro de transição de estado: Transition 'inicia_fluxo'"
                                         " isn't available from state 'DRE_A_VALIDAR'."}


def test_url_endpoint_alt_card_dre_valida(client_autenticado, alteracao_cardapio_dre_validar):
    assert str(alteracao_cardapio_dre_validar.status) == PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR
    response = client_autenticado.patch(
        f'/{ENDPOINT_ALTERACAO_CARD}/{alteracao_cardapio_dre_validar.uuid}/{constants.DRE_VALIDA_PEDIDO}/'
    )

    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json['status'] == PedidoAPartirDaEscolaWorkflow.DRE_VALIDADO
    assert str(json['uuid']) == str(alteracao_cardapio_dre_validar.uuid)


def test_url_endpoint_alt_card_dre_valida_error(client_autenticado, alteracao_cardapio):
    assert str(alteracao_cardapio.status) == PedidoAPartirDaEscolaWorkflow.RASCUNHO
    response = client_autenticado.patch(
        f'/{ENDPOINT_ALTERACAO_CARD}/{alteracao_cardapio.uuid}/{constants.DRE_VALIDA_PEDIDO}/'
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': "Erro de transição de estado: Transition 'dre_valida'"
                                         " isn't available from state 'RASCUNHO'."}


def test_url_endpoint_alt_card_dre_nao_valida(client_autenticado, alteracao_cardapio_dre_validar):
    assert str(alteracao_cardapio_dre_validar.status) == PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR
    response = client_autenticado.patch(
        f'/{ENDPOINT_ALTERACAO_CARD}/{alteracao_cardapio_dre_validar.uuid}/{constants.DRE_NAO_VALIDA_PEDIDO}/'
    )

    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json['status'] == PedidoAPartirDaEscolaWorkflow.DRE_NAO_VALIDOU_PEDIDO_ESCOLA
    assert str(json['uuid']) == str(alteracao_cardapio_dre_validar.uuid)


def test_url_endpoint_alt_card_dre_nao_valida_error(client_autenticado, alteracao_cardapio_dre_validado):
    assert str(alteracao_cardapio_dre_validado.status) == PedidoAPartirDaEscolaWorkflow.DRE_VALIDADO
    response = client_autenticado.patch(
        f'/{ENDPOINT_ALTERACAO_CARD}/{alteracao_cardapio_dre_validado.uuid}/{constants.DRE_NAO_VALIDA_PEDIDO}/'
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': "Erro de transição de estado: Transition 'dre_nao_valida' "
                                         "isn't available from state 'DRE_VALIDADO'."}


def test_url_endpoint_alt_card_codae_autoriza(client_autenticado, alteracao_cardapio_dre_validado):
    assert str(alteracao_cardapio_dre_validado.status) == PedidoAPartirDaEscolaWorkflow.DRE_VALIDADO
    response = client_autenticado.patch(
        f'/{ENDPOINT_ALTERACAO_CARD}/{alteracao_cardapio_dre_validado.uuid}/{constants.CODAE_AUTORIZA_PEDIDO}/'
    )

    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json['status'] == PedidoAPartirDaEscolaWorkflow.CODAE_AUTORIZADO
    assert str(json['uuid']) == str(alteracao_cardapio_dre_validado.uuid)


def test_url_endpoint_alt_card_codae_autoriza_error(client_autenticado, alteracao_cardapio):
    assert str(alteracao_cardapio.status) == PedidoAPartirDaEscolaWorkflow.RASCUNHO
    response = client_autenticado.patch(
        f'/{ENDPOINT_ALTERACAO_CARD}/{alteracao_cardapio.uuid}/{constants.CODAE_AUTORIZA_PEDIDO}/'
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': "Erro de transição de estado: Transition 'codae_autoriza_questionamento' "
                                         "isn't available from state 'RASCUNHO'."}


def test_url_endpoint_alt_card_codae_nega(client_autenticado, alteracao_cardapio_dre_validado):
    assert str(alteracao_cardapio_dre_validado.status) == PedidoAPartirDaEscolaWorkflow.DRE_VALIDADO
    response = client_autenticado.patch(
        f'/{ENDPOINT_ALTERACAO_CARD}/{alteracao_cardapio_dre_validado.uuid}/{constants.CODAE_NEGA_PEDIDO}/'
    )

    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json['status'] == PedidoAPartirDaEscolaWorkflow.CODAE_NEGOU_PEDIDO
    assert str(json['uuid']) == str(alteracao_cardapio_dre_validado.uuid)


def test_url_endpoint_alt_card_codae_nega_error(client_autenticado, alteracao_cardapio_codae_autorizado):
    assert str(alteracao_cardapio_codae_autorizado.status) == PedidoAPartirDaEscolaWorkflow.CODAE_AUTORIZADO
    response = client_autenticado.patch(
        f'/{ENDPOINT_ALTERACAO_CARD}/{alteracao_cardapio_codae_autorizado.uuid}/{constants.CODAE_NEGA_PEDIDO}/'
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': "Erro de transição de estado: Transition 'codae_nega_questionamento'"
                                         " isn't available from state 'CODAE_AUTORIZADO'."}


def test_url_endpoint_alt_card_terceirizada_ciencia(client_autenticado, alteracao_cardapio_codae_autorizado):
    assert str(alteracao_cardapio_codae_autorizado.status) == PedidoAPartirDaEscolaWorkflow.CODAE_AUTORIZADO
    response = client_autenticado.patch(
        f'/{ENDPOINT_ALTERACAO_CARD}/{alteracao_cardapio_codae_autorizado.uuid}/{constants.TERCEIRIZADA_TOMOU_CIENCIA}/'
    )

    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json['status'] == PedidoAPartirDaEscolaWorkflow.TERCEIRIZADA_TOMOU_CIENCIA
    assert str(json['uuid']) == str(alteracao_cardapio_codae_autorizado.uuid)


def test_url_endpoint_alt_card_terceirizada_ciencia_error(client_autenticado, alteracao_cardapio):
    assert str(alteracao_cardapio.status) == PedidoAPartirDaEscolaWorkflow.RASCUNHO
    response = client_autenticado.patch(
        f'/{ENDPOINT_ALTERACAO_CARD}/{alteracao_cardapio.uuid}/{constants.TERCEIRIZADA_TOMOU_CIENCIA}/'
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'detail': "Erro de transição de estado: Transition 'terceirizada_toma_ciencia'"
                  " isn't available from state 'RASCUNHO'."}


def test_url_endpoint_get_vinculos_tipo_alimentacao(client_autenticado, vinculo_tipo_alimentacao):
    response = client_autenticado.get(
        f'/{ENDPOINT_VINCULOS_ALIMENTACAO}/'
    )
    assert response.status_code == status.HTTP_200_OK
    json = response.json()['results']
    assert json[0]['uuid'] == str(vinculo_tipo_alimentacao.uuid)
    assert json[0]['periodo_escolar']['uuid'] == str(vinculo_tipo_alimentacao.periodo_escolar.uuid)
    assert json[0]['tipo_unidade_escolar']['uuid'] == str(vinculo_tipo_alimentacao.tipo_unidade_escolar.uuid)
    assert len(json[0]['combos']) == 5

    # testa endpoint de filtro tipo_ue
    response = client_autenticado.get(
        f'/{ENDPOINT_VINCULOS_ALIMENTACAO}/tipo_unidade_escolar/{vinculo_tipo_alimentacao.tipo_unidade_escolar.uuid}/',
    )
    json = response.json()['results']
    assert json[0]['uuid'] == str(vinculo_tipo_alimentacao.uuid)
    assert json[0]['periodo_escolar']['uuid'] == str(vinculo_tipo_alimentacao.periodo_escolar.uuid)
    assert json[0]['tipo_unidade_escolar']['uuid'] == str(vinculo_tipo_alimentacao.tipo_unidade_escolar.uuid)
    assert len(json[0]['combos']) == 5
