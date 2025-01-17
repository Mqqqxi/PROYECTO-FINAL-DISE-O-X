from django.db import models
from apps.pacientes.models import Paciente
from apps.persona.models import Nutricionista

# Create your models here.
class Progreso(models.Model):
    paciente = models.OneToOneField(Paciente,on_delete=models.CASCADE, related_name='progreso')
    nutricionista = models.OneToOneField(Nutricionista, on_delete=models.CASCADE)
    idProceso = models.AutoField(primary_key=True)
    foto = models.ImageField(upload_to='fotos_progreso/', null=True, blank=True)
    comentario = models.TextField(null=True, blank=True)
    FechaProg = models.DateField()
    PesoActual = models.FloatField()

    class Meta:
        db_table = 'Progreso'
