from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import Persona

@receiver(post_save, sender=Persona)
def assign_paciente_group(sender, instance, created, **kwargs):
    if created and instance.is_paciente:
        try:
            pacientes_group = Group.objects.get(name='Pacientes')
            instance.groups.add(pacientes_group)
        except Group.DoesNotExist:
            # Opcional: Crear el grupo si no existe
            pacientes_group = Group.objects.create(name='Pacientes')
            instance.groups.add(pacientes_group)



            