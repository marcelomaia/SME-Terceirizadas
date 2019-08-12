# Generated by Django 2.0.13 on 2019-08-09 11:52

import datetime
from django.db import migrations, models
import django.utils.timezone
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('terceirizada', '0004_merge_20190807_1832'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='edital',
            name='ativo',
        ),
        migrations.RemoveField(
            model_name='edital',
            name='data_final',
        ),
        migrations.RemoveField(
            model_name='edital',
            name='data_inicial',
        ),
        migrations.RemoveField(
            model_name='edital',
            name='descricao',
        ),
        migrations.RemoveField(
            model_name='edital',
            name='nome',
        ),
        migrations.AddField(
            model_name='edital',
            name='numero',
            field=models.CharField(default=django.utils.timezone.now, help_text='Número do Edital', max_length=100, verbose_name='Edital No'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='edital',
            name='objeto',
            field=models.TextField(default=datetime.datetime(2019, 8, 9, 11, 51, 23, 898326, tzinfo=utc), verbose_name='objeto resumido'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='edital',
            name='processo',
            field=models.CharField(default=datetime.datetime(2019, 8, 9, 11, 51, 46, 994633, tzinfo=utc), help_text='Processo administrativo do contrato', max_length=100, verbose_name='Processo Administrativo'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='edital',
            name='tipo_contratacao',
            field=models.CharField(default=datetime.datetime(2019, 8, 9, 11, 52, 3, 404146, tzinfo=utc), max_length=100, verbose_name='Tipo de contratação'),
            preserve_default=False,
        ),
    ]
