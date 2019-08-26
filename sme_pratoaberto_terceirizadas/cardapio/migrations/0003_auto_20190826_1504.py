# Generated by Django 2.0.13 on 2019-08-26 18:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('terceirizada', '0001_initial'),
        ('escola', '0001_initial'),
        ('cardapio', '0002_auto_20190826_1504'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='inversaocardapio',
            name='criado_por',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='inversaocardapio',
            name='escola',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='escola.Escola'),
        ),
        migrations.AddField(
            model_name='gruposuspensaoalimentacao',
            name='criado_por',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='gruposuspensaoalimentacao',
            name='escola',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='escola.Escola'),
        ),
        migrations.AddField(
            model_name='cardapio',
            name='edital',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='editais', to='terceirizada.Edital'),
        ),
        migrations.AddField(
            model_name='cardapio',
            name='tipos_alimentacao',
            field=models.ManyToManyField(to='cardapio.TipoAlimentacao'),
        ),
        migrations.AddField(
            model_name='alteracaocardapio',
            name='escola',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='escola.Escola'),
        ),
        migrations.AddField(
            model_name='alteracaocardapio',
            name='motivo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='cardapio.MotivoAlteracaoCardapio'),
        ),
    ]
