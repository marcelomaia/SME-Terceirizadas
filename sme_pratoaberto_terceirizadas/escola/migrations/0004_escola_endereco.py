# Generated by Django 2.0.13 on 2019-07-12 17:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dados_comuns', '0002_contato_endereco'),
        ('escola', '0003_auto_20190712_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='escola',
            name='endereco',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='dados_comuns.Endereco'),
            preserve_default=False,
        ),
    ]
