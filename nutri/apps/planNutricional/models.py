from collections import defaultdict
from django.db import models
from apps.comida.models import Plato, PlatoComida
from apps.pacientes.models import Paciente
from apps.persona.models import Nutricionista
from django.utils.timezone import now

# Create your models here.
class PlanNutricional(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="planes_nutricionales")
    idPlanN = models.AutoField(primary_key=True)
    fecha_inicio = models.DateTimeField(default=now, verbose_name="Fecha inicio")  # Se agrega `default=now`
    duracion_dias = models.PositiveIntegerField(verbose_name="Duración en Días", default=30)
    recomendacion = models.TextField()
    nutricionista = models.ForeignKey(Nutricionista, on_delete=models.CASCADE, related_name="planes_creados", null=True, blank=True)

class PlanDelDia(models.Model):
    TIPO_CHOICES = [
        ('DESAYUNO', 'Desayuno'),
        ('ALMUERZO', 'Almuerzo'),
        ('MERIENDA', 'Merienda'),
        ('CENA', 'Cena'),
    ]
    
    plan_nutricional = models.ForeignKey(PlanNutricional, on_delete=models.CASCADE, related_name="comidas")
    dia = models.PositiveIntegerField(verbose_name="Día del Plan")
    tipo_comida = models.CharField(max_length=10, choices=TIPO_CHOICES)
    plato = models.ForeignKey(PlatoComida, on_delete=models.CASCADE, verbose_name="Nombre del Plato")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción o Detalles")
    
    class Meta:
        unique_together = ('plan_nutricional', 'dia', 'tipo_comida')
        ordering = ['dia', 'tipo_comida']
    
    def __str__(self):
        return f"Día {self.dia} - {self.get_tipo_comida_display()}: {self.plato}"    


# pk=2; #agarramos el id del paciente q viene por el datatable
# plan = PlanNutricional(id_paciente=pk) #buscamos el plan del paciente
# dias = PlanDelDia.all; #agarramos todas los planes 

# if(plan_nutricional = id_plan) #buscamos solamente las comidas del plan del paciente
#     comidasfiltadas=comida;






    