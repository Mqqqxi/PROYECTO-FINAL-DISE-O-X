from django.db import models


class Comida(models.Model):
    idcomida = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='static/images/comidas/', null=True, blank=True)
    calorias = models.IntegerField()
    colesterol = models.FloatField()
    proteina = models.FloatField()
    carbohidratos = models.FloatField()
    grasaPolinsaturadas = models.FloatField()
    grasaMoninsaturadas = models.FloatField()
    grasaTrans = models.FloatField()
    grasaTotales = models.FloatField()
    grasaSaturadas = models.FloatField()
    fibraAlimentaria = models.FloatField()
    sodio = models.FloatField()
    reqEnergetico = models.FloatField()
    categoria = models.CharField(max_length=100)

    class Meta:
        db_table = 'Comida'


class Plato(models.Model):
    idplato = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(
        max_length=50,
        choices=[('desayuno', 'Desayuno'), ('almuerzo', 'Almuerzo'), ('cena', 'Cena'), ('merienda', 'Merienda')]
    )
    descripcion = models.TextField(blank=True, null=True)

    def suma_calorias(self):
        """Calcula la suma de calorías de todas las comidas en el plato."""
        return sum(relacion.calorias_segun_peso() for relacion in self.platocomida_set.all())

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"

    class Meta:
        verbose_name = "Plato"
        verbose_name_plural = "Platos"
        db_table = 'Plato'

class PlatoComida(models.Model):
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE, related_name="platocomida_set")
    comida = models.ForeignKey(Comida, on_delete=models.CASCADE)
    peso = models.FloatField(default=100)  # Peso en gramos para esta comida en el plato

    def calorias_segun_peso(self):
        """Calcula las calorías de esta comida según su peso en el plato."""
        return (self.comida.calorias * self.peso) / 100

    def __str__(self):
        return f"{self.comida.nombre} ({self.peso}g) en {self.plato.nombre}"
    
    class Meta:
        db_table = 'PlatoComida'
