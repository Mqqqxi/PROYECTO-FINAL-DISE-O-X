from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Persona, Nutricionista

# Registrar el modelo Persona con una configuración personalizada
@admin.register(Persona)
class PersonaAdmin(UserAdmin):
    # Campos a mostrar en la lista de usuarios
    list_display = ('email', 'first_name', 'last_name', 'numDocumento', 'is_paciente', 'is_nutricionista', 'is_staff')
    list_filter = ('is_paciente', 'is_nutricionista', 'is_staff')
    search_fields = ('email', 'numDocumento', 'first_name', 'last_name')

    # Campos en el formulario de edición
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name', 'numDocumento', 'tipoDocumento', 'fechaNacimiento', 'genero', 'direccion', 'telefono')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Roles', {'fields': ('is_paciente', 'is_nutricionista')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'numDocumento', 'tipoDocumento', 'fechaNacimiento', 'genero'),
        }),
    )

    # Campo usado para identificar al usuario
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

# Registrar el modelo Nutricionista
@admin.register(Nutricionista)
class NutricionistaAdmin(admin.ModelAdmin):
    list_display = ('persona', 'matricula')
    search_fields = ('persona__email', 'matricula')
