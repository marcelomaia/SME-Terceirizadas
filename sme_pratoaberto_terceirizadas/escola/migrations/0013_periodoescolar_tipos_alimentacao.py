# Generated by Django 2.0.13 on 2019-07-30 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cardapio', '0016_auto_20190729_1521'),
        ('escola', '0012_auto_20190726_1134'),
    ]

    operations = [
        migrations.AddField(
            model_name='periodoescolar',
            name='tipos_alimentacao',
            field=models.ManyToManyField(related_name='periodos_escolares', to='cardapio.TipoAlimentacao'),
        ),
    ]