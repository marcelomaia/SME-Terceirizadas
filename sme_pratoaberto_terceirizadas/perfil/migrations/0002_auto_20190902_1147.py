# Generated by Django 2.0.13 on 2019-09-02 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grupoperfil',
            name='descricao',
            field=models.TextField(blank=True, default='', verbose_name='Descricao'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='grupoperfil',
            name='nome',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='Nome'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='perfil',
            name='descricao',
            field=models.TextField(blank=True, default='', verbose_name='Descricao'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='perfil',
            name='nome',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='Nome'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='permissao',
            name='nome',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='Nome'),
            preserve_default=False,
        ),
    ]
