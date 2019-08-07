# Generated by Django 2.0.13 on 2019-08-05 14:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cardapio', '0003_auto_20190805_1003'),
    ]

    operations = [
        migrations.AddField(
            model_name='inversaocardapio',
            name='criado_por',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='inversaocardapio',
            name='observacao',
            field=models.TextField(blank=True, null=True, verbose_name='Observação'),
        ),
    ]