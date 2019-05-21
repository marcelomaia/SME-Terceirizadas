from django.db import models
from django.utils.translation import ugettext_lazy as _


class Describable(models.Model):
    name = models.CharField(_("Name"), blank=True, null=True, max_length=50)
    description = models.TextField(_("Description"), blank=True, null=True, max_length=256)

    class Meta:
        abstract = True


class Activable(models.Model):
    is_active = models.BooleanField(_("Is active"))

    class Meta:
        abstract = True


class TimestampAble(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class IntervaloDeTempo(models.Model):
    data_hora_inicial = models.DateTimeField(auto_now_add=True)
    data_hora_final = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class IntervaloDeDia(models.Model):
    data_inicial = models.DateField()
    data_final = models.DateField()

    class Meta:
        abstract = True
