# Generated by Django 2.2.6 on 2019-12-13 16:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('terceirizada', '0002_nutricionista_admin'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='nutricionista',
            options={'ordering': ['-admin'], 'verbose_name': 'Nutricionista', 'verbose_name_plural': 'Nutricionistas'},
        ),
    ]