# Generated by Django 5.1 on 2025-04-17 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planNutricional', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plandeldia',
            name='platos',
            field=models.JSONField(default=list),
        ),
    ]
