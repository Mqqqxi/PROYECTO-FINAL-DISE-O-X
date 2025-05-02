from django.urls import path
from . import views

app_name = 'turnos'

urlpatterns = [
	
	path('', views.Turnos, name = 'turnos'),
	path('reservar_turnos', views.reservar_turnos, name = 'reservar_turno'),
    path('obtener_turno', views.obtener_turno, name='obtener_turno'),
    path('cancelar_turno', views.cancelar_turno, name='cancelar_turno'),
    path('obtener_horarios_ocupados/', views.obtener_horarios_ocupados, name='obtener_horarios_ocupados'),
    path('turnos-dia/', views.obtener_turnos_dia, name='obtener_turnos_dia'),
	
]