# Generated by Django 2.0.13 on 2019-09-19 15:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('inclusao_alimentacao', '0005_auto_20190911_1002'),
    ]

    operations = [
        migrations.AddField(
            model_name='grupoinclusaoalimentacaonormal',
            name='criado_em',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Criado em'),
            preserve_default=False,
        ),
    ]
