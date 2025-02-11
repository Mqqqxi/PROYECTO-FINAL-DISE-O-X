from django.db import models
from apps.comida.models import Plato
from apps.pacientes.models import Paciente
from apps.persona.models import Nutricionista

# Create your models here.
class PlanNutricional(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="planes_nutricionales")
    idPlanN = models.AutoField(primary_key=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    duracion_dias = models.PositiveIntegerField(verbose_name="Duración en Días", default=30)
    recomendacion = models.TextField()
    platos = models.ManyToManyField(Plato, related_name='planes_nutricionales')
    nutricionista = models.ForeignKey(Nutricionista, on_delete=models.CASCADE, related_name="planes_creados")
    
    class Meta:
        db_table = 'planNutricional'

    




    