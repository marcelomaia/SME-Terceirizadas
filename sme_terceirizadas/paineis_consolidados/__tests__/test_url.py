from freezegun import freeze_time
from rest_framework import status

from ...dados_comuns.constants import SEM_FILTRO
from ..api.constants import AUTORIZADOS, CANCELADOS, NEGADOS, PENDENTES_AUTORIZACAO


def base_codae(client_autenticado, resource):
    endpoint = f'/codae-solicitacoes/{resource}/'
    response = client_autenticado.get(endpoint)
    assert response.status_code == status.HTTP_200_OK


def test_url_endpoint_painel_codae_pendentes_autorizacao(client_autenticado):
    base_codae(client_autenticado, f'{PENDENTES_AUTORIZACAO}/{SEM_FILTRO}')


def test_url_endpoint_painel_codae_aprovados(client_autenticado):
    base_codae(client_autenticado, AUTORIZADOS)


def test_url_endpoint_painel_codae_cancelados(client_autenticado):
    base_codae(client_autenticado, CANCELADOS)


def test_url_endpoint_painel_codae_negados(client_autenticado):
    base_codae(client_autenticado, NEGADOS)


def test_dieta_especial_solicitacoes_viewset_pendentes(client_autenticado,
                                                       solicitacoes_dieta_especial,
                                                       status_and_endpoint):
    wf_status, endpoint = status_and_endpoint
    response = client_autenticado.get(f'/dieta-especial/{endpoint}/')
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json['count'] == 2
    for solicitacao in json['results']:
        assert solicitacao['status_solicitacao'] == wf_status


@freeze_time('2019-10-11')
def test_escola_relatorio_evolucao_solicitacoes(users_diretor_escola):
    client, email, password, rf, cpf, user = users_diretor_escola
    response = client.get(
        f'/escola-relatorio/evolucao_solicitacoes/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'results': {
            'total': 8,
            'Inclusão de Alimentação': {
                'quantidades': [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],  # [jan, fev, mar, abr...]
                'total': 3
            },
            'Suspensão de Alimentação': {
                'quantidades': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                'total': 0
            },
            'Inversão de dia de Cardápio': {
                'quantidades': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                'total': 0
            },
            'Kit Lanche Passeio': {
                'quantidades': [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                'total': 2
            },
            'Alteração de Cardápio': {
                'quantidades': [0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0],
                'total': 3
            }
        }
    }
