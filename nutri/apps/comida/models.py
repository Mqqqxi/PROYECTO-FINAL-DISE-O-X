from django.db import models


class Comida(models.Model):
    idcomida = models.AutoField(primary_key=True)  # ID único de comida
    
    nombre = models.CharField(max_length=100)  # Nombre de la comida
    imagen = models.ImageField(upload_to='comidas/', null=True, blank=True)  # Imagen de la comida
    calorias = models.IntegerField()  # Calorias de la comida
    colesterol = models.FloatField()  # Colesterol de la comida
    proteina = models.FloatField()  # Proteinas de la comida
    carbohidratos = models.FloatField()  # Carbohidratos de la comida
    grasaPolinsaturadas = models.FloatField()  # Grasas poliinsaturadas
    grasaMoninsaturadas = models.FloatField()  # Grasas monoinsaturadas
    grasaTrans = models.FloatField()  # Grasas trans
    grasaTotales = models.FloatField()  # Grasas totales
    grasaSaturadas = models.FloatField()  # Grasas saturadas
    fibraAlimentaria = models.FloatField()  # Fibra alimentaria
    sodio = models.FloatField()  # Sodio
    reqEnergetico = models.FloatField()  # Requerimiento energetico

    class Meta:
        db_table = 'Comida'
