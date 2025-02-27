from django.urls import path
from . import views

app_name = 'plannutricional'

urlpatterns = [
	
    path('crear_plan/<int:persona_id>/', views.crear_plan_nutricional, name='crear_plan_nutricional'),
	path("crear_plan_dia/<int:paciente_id>/", views.crear_plan_dia, name="crear_plan_dia")
]

