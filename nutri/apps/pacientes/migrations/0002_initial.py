# Generated by Django 5.1 on 2025-01-16 13:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pacientes', '0001_initial'),
        ('persona', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('persona', models.OneToOneField(db_column='Persona_idPersona', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('obraSocial', models.CharField(max_length=45, null=True)),
            ],
            options={
                'db_table': 'paciente',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='historiaclinica',
            name='paciente',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='historia_clinica', to='pacientes.paciente'),
        ),
        migrations.AddField(
            model_name='anamnesis',
            name='paciente',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='anamnesis', to='pacientes.paciente'),
        ),
        migrations.AddField(
            model_name='analisislab',
            name='paciente',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='analisis_lab', to='pacientes.paciente'),
        ),
        migrations.AlterUniqueTogether(
            name='historiaclinica',
            unique_together={('paciente', 'idHistoriaClinica')},
        ),
        migrations.AlterUniqueTogether(
            name='anamnesis',
            unique_together={('paciente', 'idAnamnesis')},
        ),
        migrations.AlterUniqueTogether(
            name='analisislab',
            unique_together={('paciente', 'idAnalisis')},
        ),
        migrations.CreateModel(
            name='ValorAntropometrico',
            fields=[
                ('idValorAntropometrico', models.AutoField(primary_key=True, serialize=False)),
                ('masaMuscular', models.DecimalField(decimal_places=2, max_digits=5)),
                ('masaGrasa', models.DecimalField(decimal_places=2, max_digits=5)),
                ('circunferencia', models.DecimalField(decimal_places=2, max_digits=5)),
                ('IMC', models.DecimalField(decimal_places=2, max_digits=5)),
                ('peso', models.DecimalField(decimal_places=2, max_digits=5)),
                ('altura', models.DecimalField(decimal_places=2, max_digits=5)),
                ('paciente', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='valores_antropometricos', to='pacientes.paciente')),
            ],
            options={
                'db_table': 'ValorAntropometrico',
                'unique_together': {('paciente', 'idValorAntropometrico')},
            },
        ),
    ]
