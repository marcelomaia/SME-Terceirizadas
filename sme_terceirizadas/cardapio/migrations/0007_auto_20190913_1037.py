# Generated by Django 2.0.13 on 2019-09-13 13:37

from django.db import migrations
import django_xworkflows.models


class Migration(migrations.Migration):

    dependencies = [
        ('cardapio', '0006_auto_20190911_1002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gruposuspensaoalimentacao',
            name='status',
            field=django_xworkflows.models.StateField(max_length=26, workflow=django_xworkflows.models._SerializedWorkflow(initial_state='RASCUNHO', name='InformativoPartindoDaEscolaWorkflow', states=['RASCUNHO', 'INFORMADO', 'TERCEIRIZADA_TOMOU_CIENCIA'])),
        ),
    ]