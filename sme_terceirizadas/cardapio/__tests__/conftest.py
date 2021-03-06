import datetime

import pytest
from faker import Faker
from model_mommy import mommy
from rest_framework.test import APIClient

from ...dados_comuns.fluxo_status import InformativoPartindoDaEscolaWorkflow, PedidoAPartirDaEscolaWorkflow
from ...dados_comuns.models import TemplateMensagem
from ..api.serializers.serializers import (
    AlteracaoCardapioSerializer,
    GrupoSuspensaoAlimentacao,
    InversaoCardapioSerializer,
    MotivoAlteracaoCardapioSerializer,
    QuantidadePorPeriodoSuspensaoAlimentacao,
    SubstituicoesAlimentacaoNoPeriodoEscolarSerializer,
    SuspensaoAlimentacaoNoPeriodoEscolar,
    SuspensaoAlimentacaoSerializer
)
from ..models import (
    AlteracaoCardapio,
    InversaoCardapio,
    MotivoAlteracaoCardapio,
    MotivoSuspensao,
    SubstituicaoAlimentacaoNoPeriodoEscolar,
    SuspensaoAlimentacao
)

fake = Faker('pt_BR')
fake.seed(420)


@pytest.fixture
def tipo_alimentacao():
    return mommy.make('cardapio.TipoAlimentacao', nome='Refeição')


@pytest.fixture
def client():
    client = APIClient()
    return client


@pytest.fixture
def cardapio_valido():
    cardapio_valido = mommy.make('Cardapio', id=1, data=datetime.date(2019, 11, 29),
                                 uuid='7a4ec98a-18a8-4d0a-b722-1da8f99aaf4b',
                                 descricao='lorem ipsum')
    return cardapio_valido


@pytest.fixture
def cardapio_valido2():
    cardapio_valido2 = mommy.make('Cardapio', id=2, data=datetime.date(2019, 12, 15),
                                  uuid='7a4ec98a-18a8-4d0a-b722-1da8f99aaf4c')
    return cardapio_valido2


@pytest.fixture
def cardapio_valido3():
    data = datetime.datetime.now() + datetime.timedelta(days=6)
    cardapio_valido = mommy.make('Cardapio', id=22, data=data.date())
    return cardapio_valido


@pytest.fixture
def cardapio_invalido():
    cardapio_invalido = mommy.prepare('Cardapio', _save_related=True, id=3, data=datetime.date(2019, 7, 2),
                                      uuid='7a4ec98a-18a8-4d0a-b722-1da8f99aaf4d')
    return cardapio_invalido


@pytest.fixture
def escola():
    lote = mommy.make('Lote')
    escola = mommy.make('Escola', lote=lote)
    return escola


@pytest.fixture
def inversao_dia_cardapio(cardapio_valido2, cardapio_valido3, escola):
    mommy.make(TemplateMensagem, assunto='TESTE INVERSAO CARDAPIO',
               tipo=TemplateMensagem.INVERSAO_CARDAPIO,
               template_html='@id @criado_em @status @link')
    return mommy.make(InversaoCardapio,
                      criado_em=datetime.date(2019, 12, 12),
                      uuid='98dc7cb7-7a38-408d-907c-c0f073ca2d13',
                      cardapio_de=cardapio_valido2,
                      cardapio_para=cardapio_valido3,
                      escola=escola)


@pytest.fixture
def inversao_dia_cardapio_dre_validar(inversao_dia_cardapio):
    inversao_dia_cardapio.status = PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR
    inversao_dia_cardapio.save()
    return inversao_dia_cardapio


@pytest.fixture
def inversao_dia_cardapio_dre_validado(inversao_dia_cardapio):
    inversao_dia_cardapio.status = PedidoAPartirDaEscolaWorkflow.DRE_VALIDADO
    inversao_dia_cardapio.save()
    return inversao_dia_cardapio


@pytest.fixture
def inversao_dia_cardapio_codae_autorizado(inversao_dia_cardapio):
    inversao_dia_cardapio.status = PedidoAPartirDaEscolaWorkflow.CODAE_AUTORIZADO
    inversao_dia_cardapio.save()
    return inversao_dia_cardapio


@pytest.fixture
def inversao_dia_cardapio2(cardapio_valido, cardapio_valido2, escola):
    mommy.make(TemplateMensagem, assunto='TESTE INVERSAO CARDAPIO',
               tipo=TemplateMensagem.INVERSAO_CARDAPIO,
               template_html='@id @criado_em @status @link')
    return mommy.make(InversaoCardapio,
                      uuid='98dc7cb7-7a38-408d-907c-c0f073ca2d13',
                      cardapio_de=cardapio_valido,
                      cardapio_para=cardapio_valido2,
                      escola=escola)


@pytest.fixture
def inversao_cardapio_serializer(escola):
    cardapio_de = mommy.make('cardapio.Cardapio')
    cardapio_para = mommy.make('cardapio.Cardapio')
    inversao_cardapio = mommy.make(InversaoCardapio, cardapio_de=cardapio_de, cardapio_para=cardapio_para,
                                   escola=escola)
    return InversaoCardapioSerializer(inversao_cardapio)


@pytest.fixture
def suspensao_alimentacao(motivo_suspensao_alimentacao):
    return mommy.make(SuspensaoAlimentacao, motivo=motivo_suspensao_alimentacao)


@pytest.fixture
def suspensao_periodo_escolar(suspensao_alimentacao):
    return mommy.make(SuspensaoAlimentacaoNoPeriodoEscolar, suspensao_alimentacao=suspensao_alimentacao)


@pytest.fixture
def grupo_suspensao_alimentacao(escola):
    mommy.make(TemplateMensagem, tipo=TemplateMensagem.SUSPENSAO_ALIMENTACAO)
    return mommy.make(GrupoSuspensaoAlimentacao, observacao='lorem ipsum', escola=escola)


@pytest.fixture
def grupo_suspensao_alimentacao_informado(grupo_suspensao_alimentacao):
    grupo_suspensao_alimentacao.status = InformativoPartindoDaEscolaWorkflow.INFORMADO
    grupo_suspensao_alimentacao.save()
    return grupo_suspensao_alimentacao


@pytest.fixture
def quantidade_por_periodo_suspensao_alimentacao():
    return mommy.make(QuantidadePorPeriodoSuspensaoAlimentacao, numero_alunos=100)


@pytest.fixture
def suspensao_alimentacao_serializer(suspensao_alimentacao):
    return SuspensaoAlimentacaoSerializer(suspensao_alimentacao)


@pytest.fixture
def motivo_alteracao_cardapio():
    return mommy.make(MotivoAlteracaoCardapio, nome='Aniversariantes do mês')


@pytest.fixture
def motivo_suspensao_alimentacao():
    return mommy.make(MotivoSuspensao, nome='Não vai ter aula')


@pytest.fixture
def motivo_alteracao_cardapio_serializer():
    motivo_alteracao_cardapio = mommy.make(MotivoAlteracaoCardapio)
    return MotivoAlteracaoCardapioSerializer(motivo_alteracao_cardapio)


@pytest.fixture
def alteracao_cardapio(escola):
    mommy.make(TemplateMensagem, tipo=TemplateMensagem.ALTERACAO_CARDAPIO)
    return mommy.make(AlteracaoCardapio,
                      escola=escola,
                      observacao='teste',
                      data_inicial=datetime.date(2019, 10, 4),
                      data_final=datetime.date(2019, 12, 31))


@pytest.fixture
def alteracao_cardapio_dre_validar(alteracao_cardapio):
    alteracao_cardapio.status = PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR
    alteracao_cardapio.save()
    return alteracao_cardapio


@pytest.fixture
def alteracao_cardapio_dre_validado(alteracao_cardapio):
    alteracao_cardapio.status = PedidoAPartirDaEscolaWorkflow.DRE_VALIDADO
    alteracao_cardapio.save()
    return alteracao_cardapio


@pytest.fixture
def alteracao_cardapio_codae_autorizado(alteracao_cardapio):
    alteracao_cardapio.status = PedidoAPartirDaEscolaWorkflow.CODAE_AUTORIZADO
    alteracao_cardapio.save()
    return alteracao_cardapio


@pytest.fixture
def substituicoes_alimentacao_periodo(escola):
    alteracao_cardapio = mommy.make(AlteracaoCardapio, escola=escola, observacao='teste')
    return mommy.make(SubstituicaoAlimentacaoNoPeriodoEscolar, uuid='59beb0ca-982a-49da-98b8-10a296f274ba',
                      alteracao_cardapio=alteracao_cardapio)


@pytest.fixture
def alteracao_cardapio_serializer(escola):
    alteracao_cardapio = mommy.make(AlteracaoCardapio, escola=escola)
    return AlteracaoCardapioSerializer(alteracao_cardapio)


@pytest.fixture
def substituicoes_alimentacao_no_periodo_escolar_serializer():
    substituicoes_alimentacao_no_periodo_escolar = mommy.make(SubstituicaoAlimentacaoNoPeriodoEscolar)
    return SubstituicoesAlimentacaoNoPeriodoEscolarSerializer(substituicoes_alimentacao_no_periodo_escolar)


@pytest.fixture(params=[
    (datetime.date(2019, 8, 10), datetime.date(2019, 10, 24),
     'Diferença entre as datas não pode ultrapassar de 60 dias'),
    (datetime.date(2019, 1, 1), datetime.date(2019, 3, 3), 'Diferença entre as datas não pode ultrapassar de 60 dias'),
    (datetime.date(2019, 1, 1), datetime.date(2019, 3, 4), 'Diferença entre as datas não pode ultrapassar de 60 dias'),
])
def datas_de_inversoes_intervalo_maior_60_dias(request):
    return request.param


@pytest.fixture(params=[
    (datetime.date(2019, 8, 10), datetime.date(2019, 10, 9), True),
    (datetime.date(2019, 1, 1), datetime.date(2019, 3, 1), True),
    (datetime.date(2019, 1, 1), datetime.date(2019, 3, 2), True),
])
def datas_de_inversoes_intervalo_entre_60_dias(request):
    return request.param


@pytest.fixture(params=[
    (datetime.date(2018, 5, 26), 'Inversão de dia de cardapio deve ser solicitada no ano corrente'),
    (datetime.date(2020, 1, 1), 'Inversão de dia de cardapio deve ser solicitada no ano corrente'),
    (datetime.date(2021, 12, 1), 'Inversão de dia de cardapio deve ser solicitada no ano corrente')
])
def data_inversao_ano_diferente(request):
    return request.param


@pytest.fixture(params=[
    (datetime.date(2019, 5, 26), True),
    (datetime.date(2019, 1, 1), True),
    (datetime.date(2019, 12, 31), True)
])
def data_inversao_mesmo_ano(request):
    return request.param


@pytest.fixture(params=[
    # dia cardapio de, dia cardapio para, status
    (datetime.date(2019, 10, 1), datetime.date(2019, 10, 5), PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR),
    (datetime.date(2019, 10, 2), datetime.date(2019, 10, 6), PedidoAPartirDaEscolaWorkflow.RASCUNHO),
    (datetime.date(2019, 10, 3), datetime.date(2019, 10, 7), PedidoAPartirDaEscolaWorkflow.DRE_PEDIU_ESCOLA_REVISAR),

    (datetime.date(2019, 10, 5), datetime.date(2019, 10, 1), PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR),
    (datetime.date(2019, 10, 6), datetime.date(2019, 10, 2), PedidoAPartirDaEscolaWorkflow.RASCUNHO),
    (datetime.date(2019, 10, 7), datetime.date(2019, 10, 3), PedidoAPartirDaEscolaWorkflow.DRE_PEDIU_ESCOLA_REVISAR),
])
def datas_inversao_vencida(request):
    return request.param


@pytest.fixture(params=[
    # dia cardapio de, dia cardapio para, status
    ((2019, 10, 4), (2019, 10, 30), PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR),
    ((2019, 10, 5), (2019, 10, 12), PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR),
    ((2019, 10, 6), (2019, 10, 13), PedidoAPartirDaEscolaWorkflow.RASCUNHO),
    ((2019, 10, 7), (2019, 10, 14), PedidoAPartirDaEscolaWorkflow.DRE_PEDIU_ESCOLA_REVISAR),

    ((2019, 10, 28), (2019, 10, 7), PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR),
    ((2019, 10, 29), (2019, 10, 8), PedidoAPartirDaEscolaWorkflow.RASCUNHO),
    ((2019, 10, 30), (2019, 10, 9), PedidoAPartirDaEscolaWorkflow.DRE_PEDIU_ESCOLA_REVISAR),
    ((2019, 10, 30), (2019, 10, 4), PedidoAPartirDaEscolaWorkflow.DRE_PEDIU_ESCOLA_REVISAR),
])
def datas_inversao_desta_semana(request):
    return request.param


@pytest.fixture(params=[
    # dia cardapio de, dia cardapio para, status
    (datetime.date(2019, 10, 29), datetime.date(2019, 11, 1), PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR),
    (datetime.date(2019, 10, 15), datetime.date(2019, 10, 31), PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR),
    (datetime.date(2019, 10, 10), datetime.date(2019, 10, 29), PedidoAPartirDaEscolaWorkflow.RASCUNHO),
    (datetime.date(2019, 10, 28), datetime.date(2019, 11, 3), PedidoAPartirDaEscolaWorkflow.DRE_PEDIU_ESCOLA_REVISAR),

    (datetime.date(2019, 10, 10), datetime.date(2019, 10, 15), PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR),
    (datetime.date(2019, 10, 15), datetime.date(2019, 10, 10), PedidoAPartirDaEscolaWorkflow.RASCUNHO),
    (datetime.date(2019, 10, 4), datetime.date(2019, 11, 4), PedidoAPartirDaEscolaWorkflow.DRE_PEDIU_ESCOLA_REVISAR),
    (datetime.date(2019, 11, 4), datetime.date(2019, 10, 4), PedidoAPartirDaEscolaWorkflow.DRE_PEDIU_ESCOLA_REVISAR),
])
def datas_inversao_deste_mes(request):
    return request.param


@pytest.fixture(params=[
    # data inicial, status
    ((2019, 10, 1), PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR),
    ((2019, 10, 2), PedidoAPartirDaEscolaWorkflow.RASCUNHO),
    ((2019, 10, 3), PedidoAPartirDaEscolaWorkflow.DRE_PEDIU_ESCOLA_REVISAR),
    ((2019, 9, 30), PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR),
    ((2019, 9, 29), PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR),
    ((2019, 9, 28), PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR),

])
def datas_alteracao_vencida(request):
    return request.param


@pytest.fixture(params=[
    # data inicial, status
    ((2019, 10, 4), PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR),
    ((2019, 10, 5), PedidoAPartirDaEscolaWorkflow.RASCUNHO),
    ((2019, 10, 6), PedidoAPartirDaEscolaWorkflow.DRE_PEDIU_ESCOLA_REVISAR),
    ((2019, 10, 7), PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR),
    ((2019, 10, 8), PedidoAPartirDaEscolaWorkflow.RASCUNHO),
    ((2019, 10, 9), PedidoAPartirDaEscolaWorkflow.DRE_PEDIU_ESCOLA_REVISAR),
])
def datas_alteracao_semana(request):
    return request.param


@pytest.fixture(params=[
    # data inicial, status
    ((2019, 10, 4), PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR),
    ((2019, 10, 10), PedidoAPartirDaEscolaWorkflow.RASCUNHO),
    ((2019, 10, 15), PedidoAPartirDaEscolaWorkflow.DRE_PEDIU_ESCOLA_REVISAR),
    ((2019, 10, 20), PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR),
    ((2019, 10, 30), PedidoAPartirDaEscolaWorkflow.RASCUNHO),
    ((2019, 11, 4), PedidoAPartirDaEscolaWorkflow.DRE_PEDIU_ESCOLA_REVISAR),
])
def datas_alteracao_mes(request):
    return request.param


@pytest.fixture(params=[
    # data do teste 14 out 2019
    # data de create, data para create, data de update, data para update
    (datetime.date(2019, 10, 25), datetime.date(2019, 11, 25),
     datetime.date(2019, 11, 24), datetime.date(2019, 11, 28)),

    (datetime.date(2019, 10, 26), datetime.date(2019, 12, 24),
     datetime.date(2019, 10, 20), datetime.date(2019, 11, 24)),

    (datetime.date(2019, 12, 25), datetime.date(2019, 12, 30),
     datetime.date(2019, 12, 15), datetime.date(2019, 12, 31)),

])
def inversao_card_params(request):
    return request.param


@pytest.fixture(params=[
    # data do teste 14 out 2019
    # data de, data para
    (datetime.date(2019, 12, 25), datetime.date(2020, 1, 10)),  # deve ser no ano corrente
    (datetime.date(2019, 10, 1), datetime.date(2019, 10, 20)),  # nao pode ser no passado
    (datetime.date(2019, 10, 17), datetime.date(2019, 12, 20)),  # nao pode ter mais de 60 dias de intervalo
    (datetime.date(2019, 10, 31), datetime.date(2019, 10, 15)),  # data de nao pode ser maior que data para

])
def inversao_card_params_error(request):
    return request.param


@pytest.fixture(params=[
    # data_inicial, data_final
    (datetime.date(2019, 10, 4), datetime.date(2019, 12, 31)),
    (datetime.date(2019, 10, 5), datetime.date(2019, 12, 31)),
    (datetime.date(2019, 10, 10), datetime.date(2019, 12, 31)),
    (datetime.date(2019, 10, 20), datetime.date(2019, 12, 31)),
    (datetime.date(2019, 10, 25), datetime.date(2019, 12, 31)),
    (datetime.date(2019, 10, 31), datetime.date(2019, 12, 31)),
    (datetime.date(2019, 11, 3), datetime.date(2019, 12, 31)),
    (datetime.date(2019, 11, 4), datetime.date(2019, 12, 31)),
])
def suspensao_alimentacao_parametros_mes(request):
    return request.param


@pytest.fixture(params=[
    # data_inicial, data_final
    (datetime.date(2019, 10, 4), datetime.date(2019, 10, 4)),
    (datetime.date(2019, 10, 4), datetime.date(2019, 10, 5)),
    (datetime.date(2019, 10, 4), datetime.date(2019, 10, 6)),
    (datetime.date(2019, 10, 4), datetime.date(2019, 10, 7)),
    (datetime.date(2019, 10, 4), datetime.date(2019, 10, 8)),
    (datetime.date(2019, 10, 4), datetime.date(2019, 10, 9)),
    (datetime.date(2019, 10, 4), datetime.date(2019, 10, 10)),
    (datetime.date(2019, 10, 4), datetime.date(2019, 10, 11)),

])
def suspensao_alimentacao_parametros_semana(request):
    return request.param


@pytest.fixture(params=[
    # data do teste 15 out 2019
    # data_inicial, data_final
    (datetime.date(2019, 10, 17), datetime.date(2019, 10, 26)),
    (datetime.date(2019, 10, 18), datetime.date(2019, 10, 26)),
    (datetime.date(2020, 10, 11), datetime.date(2019, 10, 26)),
])
def alteracao_card_params(request):
    alimentacao1 = mommy.make('cardapio.TipoAlimentacao')
    alimentacao2 = mommy.make('cardapio.TipoAlimentacao')
    alimentacao3 = mommy.make('cardapio.TipoAlimentacao')
    alimentacao4 = mommy.make('cardapio.TipoAlimentacao')
    alimentacao5 = mommy.make('cardapio.TipoAlimentacao')

    alimentacao1.substituicoes.set([alimentacao2, alimentacao3, alimentacao4, alimentacao5])
    alimentacao2.substituicoes.set([alimentacao1, alimentacao3, alimentacao4, alimentacao5])
    alimentacao3.substituicoes.set([alimentacao1, alimentacao2, alimentacao4, alimentacao5])
    alimentacao4.substituicoes.set([alimentacao1, alimentacao2, alimentacao3, alimentacao5])
    alimentacao5.substituicoes.set([])

    data_inicial, data_final = request.param
    return data_inicial, data_final, alimentacao1, alimentacao2, alimentacao3, alimentacao4, alimentacao5


@pytest.fixture(params=[
    # data do teste 14 out 2019
    # data de, data para
    (datetime.date(2019, 12, 25), datetime.date(2020, 1, 10)),  # deve ser no ano corrente
    (datetime.date(2019, 10, 1), datetime.date(2019, 10, 20)),  # nao pode ser no passado
    (datetime.date(2019, 10, 17), datetime.date(2019, 12, 20)),  # nao pode ter mais de 60 dias de intervalo
    (datetime.date(2019, 10, 31), datetime.date(2019, 10, 15)),  # data de nao pode ser maior que data para

])
def grupo_suspensao_alimentacao_params(request):
    return request.param


@pytest.fixture
def tipo_unidade_escolar():
    cardapio1 = mommy.make('cardapio.Cardapio', data=datetime.date(2019, 10, 11))
    cardapio2 = mommy.make('cardapio.Cardapio', data=datetime.date(2019, 10, 15))
    return mommy.make('TipoUnidadeEscolar',
                      iniciais=fake.name()[:10],
                      cardapios=[cardapio1, cardapio2])


@pytest.fixture
def periodo_escolar():
    return mommy.make('PeriodoEscolar')


@pytest.fixture(params=[
    # periodo escolar, tipo unidade escolar
    ('MANHA', 'EMEF'),
    ('MANHA', 'CIEJA'),
])
def vinculo_tipo_alimentacao(request):
    nome_periodo, nome_ue = request.param
    alimentacoes = mommy.make('TipoAlimentacao', _quantity=4)
    combos = mommy.make('ComboDoVinculoTipoAlimentacaoPeriodoTipoUE', tipos_alimentacao=alimentacoes, _quantity=5)
    tipo_unidade_escolar = mommy.make('TipoUnidadeEscolar', iniciais=nome_ue)
    periodo_escolar = mommy.make('PeriodoEscolar', nome=nome_periodo)
    return mommy.make('VinculoTipoAlimentacaoComPeriodoEscolarETipoUnidadeEscolar', combos=combos,
                      tipo_unidade_escolar=tipo_unidade_escolar,
                      periodo_escolar=periodo_escolar)
