# Generated by Django 2.0.13 on 2019-07-25 13:09

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cardapio', '0009_suspensaoalimentacao_criado_por'),
    ]

    operations = [
        migrations.CreateModel(
            name='MotivoAlteracaoCardapio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=50, null=True, verbose_name='Nome')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
            ],
            options={
                'verbose_name': 'Motivo de alteração de cardápio',
                'verbose_name_plural': 'Motivos de alteração de cardápio',
            },
        ),
    ]
