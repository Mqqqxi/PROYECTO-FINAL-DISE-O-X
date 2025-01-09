from django.db import models
from apps.pacientes.models import Paciente

# Create your models here.
class Turno(models.Model):
    paciente = models.OneToOneField(Paciente,on_delete=models.CASCADE, related_name='turno')
    idTurno = models.AutoField(primary_key=True)
    dia = models.CharField(max_length=20)
    hora = models.TimeField()
    motivo = models.TextField()

    class Meta:
        db_table = 'Turno'