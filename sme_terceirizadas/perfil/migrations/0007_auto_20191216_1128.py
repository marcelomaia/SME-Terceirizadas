# Generated by Django 2.2.8 on 2019-12-16 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0006_auto_20191216_1107'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usuario',
            options={'ordering': ('-super_admin_terceirizadas',)},
        ),
    ]