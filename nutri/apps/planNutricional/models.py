from django.db import models
from apps.comida.models import Comida
from apps.pacientes.models import Paciente
from apps.persona.models import Nutricionista

# Create your models here.
class PlanNutricional(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="planes")
    idPlanN = models.AutoField(primary_key=True)
    dia = models.CharField(max_length=20)
    hora = models.TimeField()
    recomendacion = models.TextField()
    comidas = models.ManyToManyField(Comida, related_name='planes_nutricionales')
    nutricionista = models.ForeignKey(Nutricionista, on_delete=models.CASCADE, related_name="nutricionista")
    class Meta:
        db_table = 'planNutricional'

    