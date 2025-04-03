from django.urls import path
from . import views

app_name = 'plannutricional'

urlpatterns = [
    path("crear_plan_dia/<int:plan_nutricional_id>/", views.crear_plan_dia, name="crear_plan_dia"),
    path("editar_plan_dia/<int:plan_nutricional_id>/", views.editar_plan_dia, name="editar_plan_dia"),
    path('eliminar_plan_nutricional/<int:plan_nutricional_id>/', views.eliminar_plan_nutricional, name='eliminar_plan_nutricional'),
    path('crear_plan_nutricional_modal/<int:paciente_id>/', views.crear_plan_nutricional_modal, name='crear_plan_nutricional_modal'),
]