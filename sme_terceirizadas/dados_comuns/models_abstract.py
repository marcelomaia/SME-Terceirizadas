import datetime
import uuid

import xworkflows
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django_xworkflows import models as xwf_models

from .constants import LIMITE_INFERIOR, LIMITE_SUPERIOR, PRIORITARIO, REGULAR
from .fluxo_status import (
    InformativoPartindoDaEscolaWorkflow, PedidoAPartirDaDiretoriaRegionalWorkflow, PedidoAPartirDaEscolaWorkflow
)
from .models import LogSolicitacoesUsuario
from .utils import eh_dia_util, enviar_notificacao_e_email, obter_dias_uteis_apos
from ..perfil import models as models_perfil


class Iniciais(models.Model):
    iniciais = models.CharField('Iniciais', blank=True, max_length=10)

    class Meta:
        abstract = True


class Descritivel(models.Model):
    descricao = models.TextField('Descricao', blank=True)

    class Meta:
        abstract = True


class Nomeavel(models.Model):
    nome = models.CharField('Nome', blank=True, max_length=50)

    class Meta:
        abstract = True


class Motivo(models.Model):
    motivo = models.TextField('Motivo', blank=True)

    class Meta:
        abstract = True


class Ativavel(models.Model):
    ativo = models.BooleanField('Está ativo?', default=True)

    class Meta:
        abstract = True


class CriadoEm(models.Model):
    criado_em = models.DateTimeField('Criado em', editable=False, auto_now_add=True)

    class Meta:
        abstract = True


class IntervaloDeTempo(models.Model):
    data_hora_inicial = models.DateTimeField('Data/hora inicial')
    data_hora_final = models.DateTimeField('Data/hora final')

    class Meta:
        abstract = True


class IntervaloDeDia(models.Model):
    data_inicial = models.DateField('Data inicial')
    data_final = models.DateField('Data final')

    class Meta:
        abstract = True


class TemData(models.Model):
    data = models.DateField('Data')

    class Meta:
        abstract = True


class TemChaveExterna(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True


class DiasSemana(models.Model):
    SEGUNDA = 0
    TERCA = 1
    QUARTA = 2
    QUINTA = 3
    SEXTA = 4
    SABADO = 5
    DOMINGO = 6

    DIAS = (
        (SEGUNDA, 'Segunda'),
        (TERCA, 'Terça'),
        (QUINTA, 'Quarta'),
        (QUARTA, 'Quinta'),
        (SEXTA, 'Sexta'),
        (SABADO, 'Sábado'),
        (DOMINGO, 'Domingo'),
    )

    dias_semana = ArrayField(
        models.PositiveSmallIntegerField(choices=DIAS,
                                         default=[],
                                         null=True, blank=True
                                         )
    )

    def dias_semana_display(self):
        result = ''
        choices = dict(self.DIAS)
        for index, value in enumerate(self.dias_semana):
            result += '{0}'.format(choices[value])
            if not index == len(self.dias_semana) - 1:
                result += ', '
        return result

    class Meta:
        abstract = True


class TempoPasseio(models.Model):
    QUATRO = 0
    CINCO_A_SETE = 1
    OITO_OU_MAIS = 2

    HORAS = (
        (QUATRO, 'Quatro horas'),
        (CINCO_A_SETE, 'Cinco a sete horas'),
        (OITO_OU_MAIS, 'Oito horas'),
    )
    tempo_passeio = models.PositiveSmallIntegerField(choices=HORAS,
                                                     null=True, blank=True)

    class Meta:
        abstract = True


class FluxoAprovacaoPartindoDaEscola(xwf_models.WorkflowEnabled, models.Model):
    workflow_class = PedidoAPartirDaEscolaWorkflow
    status = xwf_models.StateField(workflow_class)
    DIAS_PARA_CANCELAR = 2

    def cancelar_pedido(self, user, justificativa=''):
        """O objeto que herdar de FluxoAprovacaoPartindoDaEscola, deve ter um property data.

        Dado dias de antecedencia de prazo, verifica se pode e altera o estado
        """
        dia_antecedencia = datetime.date.today() + datetime.timedelta(days=self.DIAS_PARA_CANCELAR)
        data_do_evento = self.data
        if isinstance(data_do_evento, datetime.datetime):
            # TODO: verificar por que os models estao retornando datetime em vez de date
            data_do_evento = data_do_evento.date()

        if (data_do_evento > dia_antecedencia) and (self.status != self.workflow_class.ESCOLA_CANCELOU):
            self.status = self.workflow_class.ESCOLA_CANCELOU
            self.salvar_log_transicao(status_evento=LogSolicitacoesUsuario.ESCOLA_CANCELOU,
                                      usuario=user,
                                      justificativa=justificativa)
            self.save()
        elif self.status == self.workflow_class.ESCOLA_CANCELOU:
            raise xworkflows.InvalidTransitionError('Já está cancelada')
        else:
            raise xworkflows.InvalidTransitionError(
                f'Só pode cancelar com no mínimo {self.DIAS_PARA_CANCELAR} dia(s) de antecedência')

    def cancelamento_automatico_apos_vencimento(self):
        """Chamado automaticamente quando o pedido já passou do dia de atendimento e não chegou ao fim do fluxo."""
        self.status = self.workflow_class.CANCELADO_AUTOMATICAMENTE

    @property
    def pode_excluir(self):
        return self.status == self.workflow_class.RASCUNHO

    @property
    def ta_na_dre(self):
        return self.status == self.workflow_class.DRE_A_VALIDAR

    @property
    def ta_na_escola(self):
        return self.status in [self.workflow_class.RASCUNHO,
                               self.workflow_class.DRE_PEDIU_ESCOLA_REVISAR]

    @property
    def ta_na_codae(self):
        return self.status == self.workflow_class.DRE_VALIDADO

    @property
    def ta_na_terceirizada(self):
        return self.status == self.workflow_class.CODAE_AUTORIZADO

    @property
    def partes_interessadas_inicio_fluxo(self):
        """

        """
        dre = self.escola.diretoria_regional
        usuarios_dre = dre.usuarios.all()
        return usuarios_dre

    @property
    def partes_interessadas_dre_valida(self):
        # TODO: filtrar usuários CODAE
        usuarios_codae = models_perfil.Usuario.objects.filter()
        return usuarios_codae

    @property
    def partes_interessadas_codae_autoriza(self):
        # TODO: filtrar usuários Terceirizadas
        usuarios_terceirizadas = models_perfil.Usuario.objects.filter()
        return usuarios_terceirizadas

    @property
    def partes_interessadas_terceirizadas_tomou_ciencia(self):
        # TODO: filtrar usuários Escolas
        usuarios_terceirizadas = models_perfil.Usuario.objects.filter()
        return usuarios_terceirizadas

    @property
    def template_mensagem(self):
        raise NotImplementedError('Deve criar um property que recupera o assunto e corpo mensagem desse objeto')

    def salvar_log_transicao(self, status_evento, usuario, **kwargs):
        raise NotImplementedError('Deve criar um método salvar_log_transicao')

    #
    # Esses hooks são chamados automaticamente após a
    # transition do status ser chamada.
    # Ex. >>> alimentacao_continua.inicia_fluxo(param1, param2, key1='val')
    #

    @xworkflows.after_transition('inicia_fluxo')
    def _inicia_fluxo_hook(self, *args, **kwargs):
        user = kwargs['user']
        assunto, corpo = self.template_mensagem
        enviar_notificacao_e_email(sender=user,
                                   recipients=self.partes_interessadas_inicio_fluxo,
                                   short_desc=assunto,
                                   long_desc=corpo)
        self.salvar_log_transicao(status_evento=LogSolicitacoesUsuario.INICIO_FLUXO,
                                  usuario=user)

    @xworkflows.after_transition('dre_valida')
    def _dre_valida_hook(self, *args, **kwargs):
        user = kwargs['user']
        if user:
            assunto, corpo = self.template_mensagem
            enviar_notificacao_e_email(sender=user,
                                       recipients=self.partes_interessadas_dre_valida,
                                       short_desc=assunto,
                                       long_desc=corpo)
            self.salvar_log_transicao(status_evento=LogSolicitacoesUsuario.DRE_VALIDOU,
                                      usuario=user)

    @xworkflows.after_transition('dre_pede_revisao')
    def _dre_pede_revisao_hook(self, *args, **kwargs):
        user = kwargs['user']
        if user:
            assunto, corpo = self.template_mensagem
            enviar_notificacao_e_email(sender=user,
                                       recipients=self.partes_interessadas_dre_valida,
                                       short_desc=assunto,
                                       long_desc=corpo)
            self.salvar_log_transicao(status_evento=LogSolicitacoesUsuario.DRE_PEDIU_REVISAO,
                                      usuario=user)

    @xworkflows.after_transition('dre_nao_valida')
    def _dre_nao_valida_hook(self, *args, **kwargs):
        user = kwargs['user']
        justificativa = kwargs.get('justificativa', '')
        if user:
            assunto, corpo = self.template_mensagem
            enviar_notificacao_e_email(sender=user,
                                       recipients=self.partes_interessadas_dre_valida,
                                       short_desc=assunto,
                                       long_desc=corpo)
            self.salvar_log_transicao(status_evento=LogSolicitacoesUsuario.DRE_NAO_VALIDOU,
                                      justificativa=justificativa,
                                      usuario=user)

    @xworkflows.after_transition('escola_revisa')
    def _escola_revisa_hook(self, *args, **kwargs):
        user = kwargs['user']
        if user:
            assunto, corpo = self.template_mensagem
            enviar_notificacao_e_email(sender=user,
                                       recipients=self.partes_interessadas_dre_valida,
                                       short_desc=assunto,
                                       long_desc=corpo)
            self.salvar_log_transicao(status_evento=LogSolicitacoesUsuario.ESCOLA_REVISOU,
                                      usuario=user)

    @xworkflows.after_transition('codae_autoriza')
    def _codae_autoriza_hook(self, *args, **kwargs):
        user = kwargs['user']
        justificativa = kwargs.get('justificativa', '')
        if user:
            assunto, corpo = self.template_mensagem
            enviar_notificacao_e_email(sender=user,
                                       recipients=self.partes_interessadas_codae_autoriza,
                                       short_desc=assunto,
                                       long_desc=corpo)
            self.salvar_log_transicao(status_evento=LogSolicitacoesUsuario.CODAE_AUTORIZOU,
                                      usuario=user,
                                      justificativa=justificativa)

    @xworkflows.after_transition('codae_nega')
    def _codae_recusou_hook(self, *args, **kwargs):
        user = kwargs['user']
        justificativa = kwargs.get('justificativa', '')
        if user:
            assunto, corpo = self.template_mensagem
            enviar_notificacao_e_email(sender=user,
                                       recipients=self.partes_interessadas_dre_valida,
                                       short_desc=assunto,
                                       long_desc=corpo)
            self.salvar_log_transicao(status_evento=LogSolicitacoesUsuario.CODAE_NEGOU,
                                      usuario=user,
                                      justificativa=justificativa)

    @xworkflows.after_transition('terceirizada_toma_ciencia')
    def _terceirizada_toma_ciencia_hook(self, *args, **kwargs):
        user = kwargs['user']
        if user:
            assunto, corpo = self.template_mensagem
            enviar_notificacao_e_email(sender=user,
                                       recipients=self.partes_interessadas_terceirizadas_tomou_ciencia,
                                       short_desc=assunto,
                                       long_desc=corpo)
            self.salvar_log_transicao(status_evento=LogSolicitacoesUsuario.TERCEIRIZADA_TOMOU_CIENCIA,
                                      usuario=user)

    class Meta:
        abstract = True


class FluxoAprovacaoPartindoDaDiretoriaRegional(xwf_models.WorkflowEnabled, models.Model):
    workflow_class = PedidoAPartirDaDiretoriaRegionalWorkflow
    status = xwf_models.StateField(workflow_class)
    DIAS_PARA_CANCELAR = 2

    def cancelar_pedido(self, user, justificativa=''):
        """O objeto que herdar de FluxoAprovacaoPartindoDaDiretoriaRegional, deve ter um property data.

        Atualmente o único pedido da DRE é o Solicitação kit lanche unificada
        Dado dias de antecedencia de prazo, verifica se pode e altera o estado
        """
        dia_antecedencia = datetime.date.today() + datetime.timedelta(days=self.DIAS_PARA_CANCELAR)
        data_do_evento = self.data
        if isinstance(data_do_evento, datetime.datetime):
            # TODO: verificar por que os models estao retornando datetime em vez de date
            data_do_evento = data_do_evento.date()

        if (data_do_evento > dia_antecedencia) and (self.status != self.workflow_class.DRE_CANCELOU):
            self.status = self.workflow_class.DRE_CANCELOU
            self.salvar_log_transicao(status_evento=LogSolicitacoesUsuario.DRE_CANCELOU,
                                      usuario=user, justificativa=justificativa)
            self.save()
        elif self.status == self.workflow_class.DRE_CANCELOU:
            raise xworkflows.InvalidTransitionError('Já está cancelada')
        else:
            raise xworkflows.InvalidTransitionError(
                f'Só pode cancelar com no mínimo {self.DIAS_PARA_CANCELAR} dia(s) de antecedência')

    @property
    def pode_excluir(self):
        return self.status == self.workflow_class.RASCUNHO

    @property
    def ta_na_dre(self):
        return self.status in [self.workflow_class.CODAE_PEDIU_DRE_REVISAR,
                               self.workflow_class.RASCUNHO]

    @property
    def ta_na_codae(self):
        return self.status == self.workflow_class.CODAE_A_AUTORIZAR

    @property
    def ta_na_terceirizada(self):
        return self.status == self.workflow_class.CODAE_AUTORIZADO

    @property
    def partes_interessadas_codae_autoriza(self):
        # TODO: filtrar usuários Terceirizadas
        usuarios_terceirizadas = models_perfil.Usuario.objects.filter()
        return usuarios_terceirizadas

    @property
    def partes_interessadas_inicio_fluxo(self):
        """TODO: retornar usuários CODAE, esse abaixo é so pra passar..."""
        dre = self.diretoria_regional
        usuarios_dre = dre.usuarios.all()
        return usuarios_dre

    @property
    def partes_interessadas_terceirizadas_tomou_ciencia(self):
        # TODO: filtrar usuários Escolas
        usuarios_terceirizadas = models_perfil.Usuario.objects.filter()
        return usuarios_terceirizadas

    @property
    def template_mensagem(self):
        raise NotImplementedError('Deve criar um property que recupera o assunto e corpo mensagem desse objeto')

    def salvar_log_transicao(self, status_evento, usuario, **kwargs):
        raise NotImplementedError('Deve criar um método salvar_log_transicao')

    @xworkflows.after_transition('inicia_fluxo')
    def _inicia_fluxo_hook(self, *args, **kwargs):
        user = kwargs['user']
        assunto, corpo = self.template_mensagem

        enviar_notificacao_e_email(sender=user,
                                   recipients=self.partes_interessadas_inicio_fluxo,
                                   short_desc=assunto,
                                   long_desc=corpo)
        self.salvar_log_transicao(status_evento=LogSolicitacoesUsuario.INICIO_FLUXO,
                                  usuario=user)

    @xworkflows.after_transition('codae_autoriza')
    def _codae_autoriza_hook(self, *args, **kwargs):
        user = kwargs['user']
        if user:
            assunto, corpo = self.template_mensagem
            enviar_notificacao_e_email(sender=user,
                                       recipients=self.partes_interessadas_codae_autoriza,
                                       short_desc=assunto,
                                       long_desc=corpo)
            self.salvar_log_transicao(status_evento=LogSolicitacoesUsuario.CODAE_AUTORIZOU,
                                      usuario=user)

    @xworkflows.after_transition('terceirizada_toma_ciencia')
    def _terceirizada_toma_ciencia_hook(self, *args, **kwargs):
        user = kwargs['user']
        if user:
            assunto, corpo = self.template_mensagem
            enviar_notificacao_e_email(sender=user,
                                       recipients=self.partes_interessadas_terceirizadas_tomou_ciencia,
                                       short_desc=assunto,
                                       long_desc=corpo)
            self.salvar_log_transicao(status_evento=LogSolicitacoesUsuario.TERCEIRIZADA_TOMOU_CIENCIA,
                                      usuario=user)

    class Meta:
        abstract = True


class FluxoInformativoPartindoDaEscola(xwf_models.WorkflowEnabled, models.Model):
    workflow_class = InformativoPartindoDaEscolaWorkflow
    status = xwf_models.StateField(workflow_class)

    @property
    def pode_excluir(self):
        return self.status == self.workflow_class.RASCUNHO

    @property
    def partes_interessadas_informacao(self):
        """TODO: retornar usuários DRE, esse abaixo é so pra passar..."""
        dre = self.escola.diretoria_regional
        usuarios_dre = dre.usuarios.all()
        return usuarios_dre

    @property
    def partes_interessadas_terceirizadas_tomou_ciencia(self):
        # TODO: filtrar usuários Escolas
        usuarios_terceirizadas = models_perfil.Usuario.objects.filter()
        return usuarios_terceirizadas

    @property
    def template_mensagem(self):
        raise NotImplementedError('Deve criar um property que recupera o assunto e corpo mensagem desse objeto')

    @xworkflows.after_transition('informa')
    def _informa_hook(self, *args, **kwargs):
        user = kwargs['user']
        assunto, corpo = self.template_mensagem
        enviar_notificacao_e_email(sender=user,
                                   recipients=self.partes_interessadas_informacao,
                                   short_desc=assunto,
                                   long_desc=corpo)
        self.salvar_log_transicao(status_evento=LogSolicitacoesUsuario.INICIO_FLUXO,
                                  usuario=user)

    @xworkflows.after_transition('terceirizada_toma_ciencia')
    def _terceirizada_toma_ciencia_hook(self, *args, **kwargs):
        user = kwargs['user']
        if user:
            assunto, corpo = self.template_mensagem
            enviar_notificacao_e_email(sender=user,
                                       recipients=self.partes_interessadas_terceirizadas_tomou_ciencia,
                                       short_desc=assunto,
                                       long_desc=corpo)
            self.salvar_log_transicao(status_evento=LogSolicitacoesUsuario.TERCEIRIZADA_TOMOU_CIENCIA,
                                      usuario=user)

    class Meta:
        abstract = True


class CriadoPor(models.Model):
    # TODO: futuramente deixar obrigatorio esse campo
    criado_por = models.ForeignKey('perfil.Usuario', on_delete=models.DO_NOTHING,
                                   null=True, blank=True)

    class Meta:
        abstract = True


class TemObservacao(models.Model):
    observacao = models.TextField('Observação', blank=True)

    class Meta:
        abstract = True


class TemIdentificadorExternoAmigavel(object):
    """Gera uma chave externa amigável, não única.

    Somente para identificar externamente.
    Obrigatoriamente o objeto deve ter um uuid
    """

    @property
    def id_externo(self):
        uuid = str(self.uuid)
        return uuid.upper()[:5]


class TemPrioridade(object):
    """Exibe o tipo de prioridade do objeto de acordo com as datas que ele tem.

    Quando o objeto implementa o TemPrioridade, ele deve ter um property data
    """

    @property
    def data(self):
        raise NotImplementedError('Deve implementar um property @data')

    @property
    def prioridade(self):
        descricao = 'VENCIDO'
        hoje = datetime.date.today()
        data_pedido = self.data

        ultimo_dia_util = self._get_ultimo_dia_util(data_pedido)
        minimo_dias_para_pedido = obter_dias_uteis_apos(hoje, PRIORITARIO)
        dias_uteis_limite_inferior = obter_dias_uteis_apos(hoje, LIMITE_INFERIOR)
        dias_uteis_limite_superior = obter_dias_uteis_apos(hoje, LIMITE_SUPERIOR)
        dias_de_prazo_regular_em_diante = obter_dias_uteis_apos(hoje, REGULAR)

        if minimo_dias_para_pedido >= ultimo_dia_util >= hoje:
            descricao = 'PRIORITARIO'
        elif dias_uteis_limite_superior >= ultimo_dia_util >= dias_uteis_limite_inferior:
            descricao = 'LIMITE'
        elif ultimo_dia_util >= dias_de_prazo_regular_em_diante:
            descricao = 'REGULAR'

        return descricao

    def _get_ultimo_dia_util(self, data: datetime.date):
        """Assumindo que é sab, dom ou feriado volta para o dia util anterior."""
        data_retorno = data
        while not eh_dia_util(data_retorno):
            data_retorno -= datetime.timedelta(days=1)
        return data_retorno


class Logs(object):
    @property
    def logs(self):
        return LogSolicitacoesUsuario.objects.filter(uuid_original=self.uuid)