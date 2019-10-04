# Generated by Django 2.0.13 on 2019-09-11 13:02

from django.db import migrations
import django_xworkflows.models


class Migration(migrations.Migration):

    dependencies = [
        ('inclusao_alimentacao', '0004_auto_20190906_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grupoinclusaoalimentacaonormal',
            name='status',
            field=django_xworkflows.models.StateField(max_length=29, workflow=django_xworkflows.models._SerializedWorkflow(initial_state='RASCUNHO', name='PedidoAPartirDaEscolaWorkflow', states=['RASCUNHO', 'DRE_A_VALIDAR', 'DRE_VALIDADO', 'DRE_PEDIU_ESCOLA_REVISAR', 'DRE_NAO_VALIDOU_PEDIDO_ESCOLA', 'CODAE_AUTORIZADO', 'CODAE_NEGOU_PEDIDO', 'TERCEIRIZADA_TOMOU_CIENCIA', 'ESCOLA_CANCELOU', 'CANCELADO_AUTOMATICAMENTE'])),
        ),
        migrations.AlterField(
            model_name='inclusaoalimentacaocontinua',
            name='status',
            field=django_xworkflows.models.StateField(max_length=29, workflow=django_xworkflows.models._SerializedWorkflow(initial_state='RASCUNHO', name='PedidoAPartirDaEscolaWorkflow', states=['RASCUNHO', 'DRE_A_VALIDAR', 'DRE_VALIDADO', 'DRE_PEDIU_ESCOLA_REVISAR', 'DRE_NAO_VALIDOU_PEDIDO_ESCOLA', 'CODAE_AUTORIZADO', 'CODAE_NEGOU_PEDIDO', 'TERCEIRIZADA_TOMOU_CIENCIA', 'ESCOLA_CANCELOU', 'CANCELADO_AUTOMATICAMENTE'])),
        ),
    ]