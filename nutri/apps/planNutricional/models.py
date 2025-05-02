from django.db import models
from django.utils.timezone import now
from apps.pacientes.models import Paciente
from apps.persona.models import Nutricionista
from django.db.models import JSONField  # JSONField genérico para MySQL

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
    # Usar JSONField genérico para MySQL
    plato1 = JSONField(default=list, blank=True, null=True, verbose_name="Platos Opción 1")  # Lista de platos en formato JSON
    plato2 = JSONField(default=list, blank=True, null=True, verbose_name="Platos Opción 2")
    plato3 = JSONField(default=list, blank=True, null=True, verbose_name="Platos Opción 3")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción o Detalles")

    class Meta:
        unique_together = ('plan_nutricional', 'dia', 'tipo_comida')
        ordering = ['dia', 'tipo_comida']

    def __str__(self):
        platos_count = len(self.plato1 or []) + len(self.plato2 or []) + len(self.plato3 or [])
        return f"Día {self.dia} - {self.get_tipo_comida_display()} - {platos_count} platos"