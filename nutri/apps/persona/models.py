from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
# Create your models here.
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# Manager personalizado
class PersonaManager(BaseUserManager):
    def create_user(self, email, fechaNacimiento,numDocumento, tipoDocumento, genero, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio.')
        if not numDocumento:
            raise ValueError('El número de documento es obligatorio.')

        email = self.normalize_email(email)
        user = self.model(email=email, fechaNacimiento=fechaNacimiento, numDocumento=numDocumento, tipoDocumento=tipoDocumento, genero=genero, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fechaNacimiento, numDocumento, tipoDocumento, genero, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, fechaNacimiento, numDocumento, tipoDocumento, genero, password, **extra_fields)

class Persona(AbstractUser):
    username=None
    #idpersona = models.AutoField(primary_key=True)  # ID único para la persona
    
    email = models.EmailField(unique=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    fechaNacimiento = models.DateField(null=True, blank=True)
    numDocumento = models.CharField(max_length=20, unique=True)  # Número de documento (DNI, cédula, etc.)
    tipoDocumento = models.CharField(max_length=10)  # Tipo de documento (DNI, pasaporte, etc.)
    genero = models.CharField(max_length=20)
    is_paciente = models.BooleanField(default=False)  # Indica si es un paciente
    is_nutricionista = models.BooleanField(default=False)  # Indica si es un nutricionista
    
    objects = PersonaManager()


    # Si prefieres usar el correo electrónico en lugar del username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'fechaNacimiento' ,'numDocumento', 'genero']


    class Meta:
        db_table = 'persona'

class Nutricionista(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, db_column='Persona_idPersona', primary_key=True)  # Field name made lowercase.
    matricula = models.CharField(max_length=45)

    class Meta:
        managed = True
        db_table = 'nutricionista'








