from django.db import models


class Comida(models.Model):
    idcomida = models.AutoField(primary_key=True)  # ID único de comida
    nombre = models.CharField(max_length=100)  # Nombre de la comida
    imagen = models.ImageField(upload_to='static/images/comidas/', null=True, blank=True)  # Imagen de la comida
    calorias = models.IntegerField()  # Calorías de la comida
    colesterol = models.FloatField()  # Colesterol de la comida
    proteina = models.FloatField()  # Proteínas de la comida
    carbohidratos = models.FloatField()  # Carbohidratos de la comida
    grasaPolinsaturadas = models.FloatField()  # Grasas poliinsaturadas
    grasaMoninsaturadas = models.FloatField()  # Grasas monoinsaturadas
    grasaTrans = models.FloatField()  # Grasas trans
    grasaTotales = models.FloatField()  # Grasas totales
    grasaSaturadas = models.FloatField()  # Grasas saturadas
    fibraAlimentaria = models.FloatField()  # Fibra alimentaria
    sodio = models.FloatField()  # Sodio
    reqEnergetico = models.FloatField()  # Requerimiento energético
    categoria = models.CharField(max_length=100)

    class Meta:
        db_table = 'Comida'


class Plato(models.Model):
    idplato = models.AutoField(primary_key=True)  # ID único del plato
    nombre = models.CharField(max_length=100)  # Nombre del plato
    tipo = models.CharField(
        max_length=50,
        verbose_name="Tipo de Plato",
        choices=[('desayuno', 'Desayuno'), ('almuerzo', 'Almuerzo'), ('cena', 'Cena'), ('merienda', 'Merienda')]
    )
    descripcion = models.TextField(
        verbose_name="Descripción del Plato", blank=True, null=True,
        help_text="Detalles específicos del plato (e.g., ingredientes)"
    )
    comida = models.ManyToManyField(Comida, verbose_name="Comida Base")  # Se elimina 'on_delete'

    def suma_calorias(self):
        """Calcula la suma de calorías de todas las comidas en el plato."""
        return sum(
            relacion.calorias_segun_peso()
            for relacion in self.platocomida_set.all()
        )

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"

    class Meta:
        verbose_name = "Plato"
        verbose_name_plural = "Platos"


class PlatoComida(models.Model):
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE, related_name="platocomida_set")
    comida = models.ForeignKey(Comida, on_delete=models.CASCADE)
    peso = models.FloatField(default=100)  # Peso en gramos para esta comida en el plato

    def calorias_segun_peso(self):
        """Calcula las calorías de esta comida según su peso en el plato."""
        return (self.comida.calorias * self.peso) / 100

    def __str__(self):
        return f"{self.comida.nombre} ({self.peso}g) en {self.plato.nombre}"
