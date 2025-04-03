from datetime import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.persona.models import Persona


from django.db import models

class Paciente(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, db_column='Persona_idPersona', primary_key=True)
    obraSocial = models.CharField(max_length=45, null=True)
    objetivo = models.CharField(
        max_length=50,
        choices=[
            ('perder_peso', 'Perder peso'),
            ('ganar_masa', 'Ganar masa muscular'),
            ('mantener', 'Mantener peso'),
            ('no_definido', 'No definido'),
        ],
        default='no_definido'
    )  # Objetivo del paciente
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)


    class Meta:
        managed= True
        db_table = 'paciente'

    def __str__(self):
        return f"{self.persona.first_name} {self.persona.last_name}"



class ValorAntropometrico(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE, related_name='valores_antropometricos')
    # La clave primaria de esta entidad será la del paciente y un identificador único.
    idValorAntropometrico = models.AutoField(primary_key=True)
    masaMuscular = models.DecimalField(max_digits=5, decimal_places=2)
    masaGrasa = models.DecimalField(max_digits=5, decimal_places=2)
    circunferencia = models.DecimalField(max_digits=5, decimal_places=2)
    IMC = models.DecimalField(max_digits=5, decimal_places=2)
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    altura = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        # Esto asegura que la combinacion de paciente y id es unica
        unique_together = ('paciente', 'idValorAntropometrico')
        db_table = 'ValorAntropometrico' 

class AnalisisLab(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE, related_name='analisis_lab')
    idAnalisis = models.AutoField(primary_key=True)
    hepatograma = models.DecimalField(max_digits=5, decimal_places=2)
    creatininaSerica = models.DecimalField(max_digits=5, decimal_places=2)
    uricemia = models.DecimalField(max_digits=5, decimal_places=2)
    colesterolTotal = models.DecimalField(max_digits=5, decimal_places=2)
    uremia = models.DecimalField(max_digits=5, decimal_places=2)
    hdl = models.DecimalField(max_digits=5, decimal_places=2)
    ldl = models.DecimalField(max_digits=5, decimal_places=2)
    trigiceridos = models.DecimalField(max_digits=5, decimal_places=2)
    glucemia = models.DecimalField(max_digits=5, decimal_places=2)
    vitaminaB12 = models.DecimalField(max_digits=5, decimal_places=2)
    albumina = models.DecimalField(max_digits=5, decimal_places=2)
    perritina = models.DecimalField(max_digits=5, decimal_places=2)
    globulosRojos = models.DecimalField(max_digits=5, decimal_places=2)
    leucositos = models.DecimalField(max_digits=5, decimal_places=2)
    hematocrito = models.DecimalField(max_digits=5, decimal_places=2)
    vitaminaD = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        # Asegura la unicidad por paciente y el identificador del análisis
        unique_together = ('paciente', 'idAnalisis')
        db_table = 'AnalisisLab' 

class Anamnesis(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE, related_name='anamnesis')
    idAnamnesis = models.AutoField(primary_key=True)
    habitos = models.CharField(max_length=100)
    preferencia = models.CharField(max_length=100)
    frecConsumo = models.CharField(max_length=100)
    registroComida = models.TextField()
    alimActual = models.TextField()

    class Meta:
        # Asegura la unicidad por paciente y el identificador de la anamnesis
        unique_together = ('paciente', 'idAnamnesis')
        db_table = 'Anamnesis' 

class HistoriaClinica(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE, related_name='historia_clinica')
    idHistoriaClinica = models.AutoField(primary_key=True)
    medicamento = models.TextField()
    suplemento = models.TextField()
    alergia = models.TextField()
    edad = models.PositiveIntegerField()
    fechaNac = models.DateField()
    intolerancia = models.TextField()
    anteFamiliar = models.TextField()
    antePatologico = models.TextField()
    patologiaActual = models.TextField()
    hsActiFisica = models.IntegerField()
    tipoActiFisica = models.TextField()
    actiLaboral = models.TextField()
    sexo = models.TextField()
    comentario = models.TextField()

    class Meta:
        unique_together = ('paciente', 'idHistoriaClinica')
        db_table = 'historiaclinica'
    