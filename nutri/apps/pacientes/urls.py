from django.urls import path
from .views import crear_datos_paciente, listapacientenuevo, registro_paciente, login_paciente, editar_perfil_paciente, mi_seguimiento,lista_pacientes, editar_paciente, deshabilitar_paciente, habilitar_paciente, listapacientenuevo, infopaciente

app_name = 'pacientes'

urlpatterns = [
    path('registro/', registro_paciente, name='registro'),
    path('login/', login_paciente, name='login'),
    path('perfil/', editar_perfil_paciente, name='perfil'),
    path('miseeguimiento/<int:persona_id>/', mi_seguimiento, name='miseeguimiento'),
    path('listapaciente/',lista_pacientes, name='listapaciente'),
    path('editar/<int:persona_id>/', editar_paciente, name='editar_paciente'),
    path('deshabilitar/<int:pk>/', deshabilitar_paciente, name='deshabilitar_paciente'),
    path('habilitar/<int:pk>/', habilitar_paciente, name='habilitar_paciente'),
    path('crear-datos/<int:persona_id>/', crear_datos_paciente, name='crear_datos_paciente'),  # Nueva URL
    path('listapacientenuevo/',listapacientenuevo, name='listapacientenuevo'),
    # el propio paciente ve su seguimiento sin pasar ID
    path("mi‑seguimiento/", infopaciente, name="infopaciente"),

    # el/la nutricionista abre la ficha de cualquier paciente
    path("paciente/<int:paciente_id>/", infopaciente, name="infopaciente_detalle"),
    
]
