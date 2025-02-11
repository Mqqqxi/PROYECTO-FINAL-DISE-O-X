from django.urls import path
from .views import registro_paciente, login_paciente, editar_perfil_paciente, seguimiento_paciente,lista_pacientes, editar_paciente, deshabilitar_paciente, habilitar_paciente

app_name = 'pacientes'

urlpatterns = [
    path('registro/', registro_paciente, name='registro'),
    path('login/', login_paciente, name='login'),
    path('perfil/', editar_perfil_paciente, name='perfil'),
    path('seguimiento/',seguimiento_paciente, name='seguimiento'),
    path('listapaciente/',lista_pacientes, name='listapaciente'),
    path('editar/<int:persona_id>/', editar_paciente, name='editar_paciente'),
    path('deshabilitar/<int:pk>/', deshabilitar_paciente, name='deshabilitar_paciente'),
    path('habilitar/<int:pk>/', habilitar_paciente, name='habilitar_paciente'),
]
