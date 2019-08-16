import datetime
from django.db import models

from sme_pratoaberto_terceirizadas.dados_comuns.utils import obter_dias_uteis_apos_hoje


class InclusoesDeAlimentacaoContinuaPrazoVencendoManager(models.Manager):
    def get_queryset(self):
        data_limite = obter_dias_uteis_apos_hoje(quantidade_dias=2)
        return super(InclusoesDeAlimentacaoContinuaPrazoVencendoManager, self).get_queryset().filter(
            data_inicial__lte=data_limite
        )


class InclusoesDeAlimentacaoContinuaPrazoVencendoHojeManager(models.Manager):
    def get_queryset(self):
        data_limite = datetime.datetime.utcnow().date()
        print(data_limite)
        return super(InclusoesDeAlimentacaoContinuaPrazoVencendoHojeManager, self).get_queryset().filter(
            data_inicial=data_limite
        )


class InclusoesDeAlimentacaoContinuaPrazoLimiteManager(models.Manager):
    def get_queryset(self):
        data_limite_inicial = obter_dias_uteis_apos_hoje(quantidade_dias=3)
        data_limite_final = obter_dias_uteis_apos_hoje(quantidade_dias=5)
        return super(InclusoesDeAlimentacaoContinuaPrazoLimiteManager, self).get_queryset().filter(
            data_inicial__range=(data_limite_inicial, data_limite_final)
        )


class InclusoesDeAlimentacaoContinuaPrazoLimiteDaquiA7DiasManager(models.Manager):
    def get_queryset(self):
        data_limite_inicial = obter_dias_uteis_apos_hoje(quantidade_dias=3)
        data_limite_final = datetime.datetime.utcnow().date() + datetime.timedelta(days=8)
        return super(InclusoesDeAlimentacaoContinuaPrazoLimiteDaquiA7DiasManager, self).get_queryset().filter(
            data_inicial__range=(data_limite_inicial, data_limite_final)
        )


class InclusoesDeAlimentacaoContinuaPrazoRegularManager(models.Manager):
    def get_queryset(self):
        data_limite = obter_dias_uteis_apos_hoje(quantidade_dias=5)
        return super(InclusoesDeAlimentacaoContinuaPrazoRegularManager, self).get_queryset().filter(
            data_inicial__gte=data_limite
        )


class InclusoesDeAlimentacaoContinuaPrazoRegularDaquiA7DiasManager(models.Manager):
    def get_queryset(self):
        data_limite_inicial = obter_dias_uteis_apos_hoje(quantidade_dias=5)
        data_limite_final = datetime.datetime.utcnow().date() + datetime.timedelta(days=8)
        return super(InclusoesDeAlimentacaoContinuaPrazoRegularDaquiA7DiasManager, self).get_queryset().filter(
            data_inicial__range=(data_limite_inicial, data_limite_final)
        )


class InclusoesDeAlimentacaoContinuaPrazoRegularDaquiA30DiasManager(models.Manager):
    def get_queryset(self):
        data_limite_inicial = obter_dias_uteis_apos_hoje(quantidade_dias=5)
        data_limite_final = datetime.datetime.utcnow().date() + datetime.timedelta(days=31)
        return super(InclusoesDeAlimentacaoContinuaPrazoRegularDaquiA30DiasManager, self).get_queryset().filter(
            data_inicial__range=(data_limite_inicial, data_limite_final)
        )


class InclusoesDeAlimentacaoNormalPrazoVencendoManager(models.Manager):
    def get_queryset(self):
        data_limite = obter_dias_uteis_apos_hoje(quantidade_dias=2)
        return super(InclusoesDeAlimentacaoNormalPrazoVencendoManager, self).get_queryset().filter(
            inclusoes_normais__data__lte=data_limite
        )


class InclusoesDeAlimentacaoNormalPrazoLimiteManager(models.Manager):
    def get_queryset(self):
        data_limite_inicial = obter_dias_uteis_apos_hoje(quantidade_dias=3)
        data_limite_final = obter_dias_uteis_apos_hoje(quantidade_dias=5)
        return super(InclusoesDeAlimentacaoNormalPrazoLimiteManager, self).get_queryset().filter(
            inclusoes_normais__data__range=(data_limite_inicial, data_limite_final)
        )


class InclusoesDeAlimentacaoNormalPrazoRegularManager(models.Manager):
    def get_queryset(self):
        data_limite = obter_dias_uteis_apos_hoje(quantidade_dias=5)
        return super(InclusoesDeAlimentacaoNormalPrazoRegularManager, self).get_queryset().filter(
            inclusoes_normais__data__gte=data_limite
        )
