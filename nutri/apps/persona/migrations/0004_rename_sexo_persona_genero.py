# Generated by Django 5.1 on 2025-04-04 14:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0003_persona_sexo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='persona',
            old_name='sexo',
            new_name='genero',
        ),
    ]
