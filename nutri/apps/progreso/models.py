from django.db import models
from apps.pacientes.models import Paciente
from apps.persona.models import Nutricionista

    
class Progreso(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='progresos')
    nutricionista = models.ForeignKey(Nutricionista, on_delete=models.CASCADE, related_name='progresos', null=True)  # Nueva clave foránea
    idProceso = models.AutoField(primary_key=True)
    fecha = models.DateField()  # Fecha del progreso (ejemplo: 2024-12-10)
    peso = models.FloatField()  # Peso en kg (ejemplo: 52.9 kg)
    comentario = models.TextField(null=True, blank=True)  # Comentario opcional

    # Datos antropométricos
    indice_grasa_corporal = models.FloatField(null=True, blank=True)  # Índice de grasa corporal
    perimetro_cintura = models.FloatField(null=True, blank=True)  # Perímetro de cintura (cm)
    perimetro_cadera = models.FloatField(null=True, blank=True)  # Perímetro de cadera (cm)
    perimetro_muslo = models.FloatField(null=True, blank=True)  # Perímetro de muslo (cm)
    perimetro_brazo = models.FloatField(null=True, blank=True)  # Perímetro de brazo (cm)
    perimetro_pecho = models.FloatField(null=True, blank=True)  # Perímetro de pecho (cm)
    masa_muscular = models.FloatField(null=True, blank=True)  # Masa muscular (kg)
    agua_corporal = models.FloatField(null=True, blank=True)  # Agua corporal (%)

    # Tensión arterial
    tension_arterial_maxima = models.FloatField(null=True, blank=True)  # Tensión arterial máxima
    tension_arterial_minima = models.FloatField(null=True, blank=True)  # Tensión arterial mínima

    class Meta:
        db_table = 'Progreso'
        ordering = ['-fecha']
        unique_together = ['paciente', 'fecha']  # Un solo progreso por paciente y fecha

    def __str__(self):
        return f"Progreso de {self.paciente.nombre} {self.paciente.apellido} - {self.fecha} ({self.peso} kg)"
    



class FotoProgreso(models.Model):
    progreso = models.ForeignKey(Progreso, on_delete=models.CASCADE, related_name='fotos')
    foto = models.ImageField(upload_to='fotos_progreso/%Y/%m/%d/')
    descripcion = models.CharField(max_length=50, blank=True, null=True)  # Ejemplo: "Frente", "Espalda", "Lado"
    creado = models.DateTimeField()

    class Meta:
        db_table = 'FotoProgreso'

    def __str__(self):
        return f"Foto de {self.progreso} - {self.descripcion if self.descripcion else 'Sin descripción'}"