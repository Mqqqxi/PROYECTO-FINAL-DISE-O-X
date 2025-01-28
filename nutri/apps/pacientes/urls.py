from django.urls import path
from .views import registro_paciente, login_paciente, editar_perfil_paciente, seguimiento_paciente,listapaciente, editar_paciente, deshabilitar_paciente

app_name = 'pacientes'

urlpatterns = [
    path('registro/', registro_paciente, name='registro'),
    path('login/', login_paciente, name='login'),
    path('perfil/', editar_perfil_paciente, name='perfil'),
    path('seguimiento/',seguimiento_paciente, name='seguimiento'),
    path('listapaciente/',listapaciente, name='listapaciente'),
    path('editar/<int:persona_id>/', editar_paciente, name='editar_paciente'),
    path('deshabilitar/<int:pk>/', deshabilitar_paciente, name='deshabilitar_paciente')
]
