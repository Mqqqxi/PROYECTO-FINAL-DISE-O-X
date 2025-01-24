from django.urls import path
from .views import registro_paciente, login_paciente, editar_perfil_paciente, seguimiento_paciente,listapaciente

app_name = 'pacientes'

urlpatterns = [
    path('registro/', registro_paciente, name='registro'),
    path('login/', login_paciente, name='login'),
    path('perfil/', editar_perfil_paciente, name='perfil'),
    path('seguimiento/',seguimiento_paciente, name='seguimiento'),
    path('listapaciente/',listapaciente, name='paciente'),
]
