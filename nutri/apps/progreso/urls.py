from django.urls import path
from . import views

app_name = 'progreso'

urlpatterns = [
	
	path('crear_progreso/<int:paciente_pk>/', views.CrearProgreso, name='crear_progreso'),
    path('obtener_datos_progreso/<int:paciente_pk>/<str:fecha>/', views.obtener_datos_progreso, name='obtener_datos_progreso'),
]