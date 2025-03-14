# Generated by Django 5.1 on 2025-03-05 13:56

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('comida', '0006_alter_plato_table_alter_platocomida_table'),
        ('pacientes', '0002_initial'),
        ('persona', '0002_persona_fechanacimiento'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlanNutricional',
            fields=[
                ('idPlanN', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_inicio', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha inicio')),
                ('duracion_dias', models.PositiveIntegerField(default=30, verbose_name='Duración en Días')),
                ('recomendacion', models.TextField()),
                ('nutricionista', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='planes_creados', to='persona.nutricionista')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='planes_nutricionales', to='pacientes.paciente')),
            ],
        ),
        migrations.CreateModel(
            name='PlanDelDia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia', models.PositiveIntegerField(verbose_name='Día del Plan')),
                ('tipo_comida', models.CharField(choices=[('DESAYUNO', 'Desayuno'), ('ALMUERZO', 'Almuerzo'), ('MERIENDA', 'Merienda'), ('CENA', 'Cena')], max_length=10)),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='Descripción o Detalles')),
                ('plato', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='planes_dia', to='comida.platocomida')),
                ('plan_nutricional', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='planes_dia', to='planNutricional.plannutricional')),
            ],
            options={
                'ordering': ['dia', 'tipo_comida'],
                'unique_together': {('plan_nutricional', 'dia', 'tipo_comida')},
            },
        ),
    ]
