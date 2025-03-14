from django.db import models
from django.utils.timezone import now
import json
from apps.pacientes.models import Paciente
from apps.persona.models import Nutricionista
from apps.comida.models import Plato

class PlanNutricional(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="planes_nutricionales")
    idPlanN = models.AutoField(primary_key=True)
    fecha_inicio = models.DateTimeField(default=now, verbose_name="Fecha inicio")
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
    
    plan_nutricional = models.ForeignKey(PlanNutricional, on_delete=models.CASCADE, related_name="planes_dia")
    dia = models.PositiveIntegerField(verbose_name="Día del Plan")
    tipo_comida = models.CharField(max_length=10, choices=TIPO_CHOICES)
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE, related_name="planes_dia", null=True)
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción o Detalles")

    class Meta:
        unique_together = ('plan_nutricional', 'dia', 'tipo_comida')
        ordering = ['dia', 'tipo_comida']

    def __str__(self):
        return f"Día {self.dia} - {self.get_tipo_comida_display()} - {self.plato.plato.nombre if self.plato else 'Sin plato'}"



