from django.db import models

class Persona(models.Model):
    idpersona = models.AutoField(primary_key=True)  # ID único para la persona
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    numDocumento = models.CharField(max_length=20, unique=True)  # Número de documento (DNI, cédula, etc.)
    tipoDocumento = models.CharField(max_length=10)  # Tipo de documento (DNI, pasaporte, etc.)

    class Meta:
        abstract = True  # Esto hace que Persona sea una clase abstracta y no cree una tabla en la DB

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Nutricionista(Persona):

    class Meta:
        db_table = 'Nutricionista' 

