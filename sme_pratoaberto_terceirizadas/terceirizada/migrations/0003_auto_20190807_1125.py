# Generated by Django 2.0.13 on 2019-08-07 14:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('terceirizada', '0002_auto_20190805_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nutricionista',
            name='terceirizada',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nutricionistas', to='terceirizada.Terceirizada'),
        ),
    ]