from django.urls import path
from . import views

app_name = 'comida'

urlpatterns = [
    path("", views.comida, name='comida'),
    path('agregar_comida/', views.agregar_comida, name='agregar_comida'),
    path('editar/<int:pk>/', views.editar_comida, name='editar_comida'),
    path('eliminar/<int:pk>/', views.eliminar_comida, name='eliminar_comida'),
    path('plato/', views.plato, name='plato'),
    path('plato/agregar_plato/', views.agregar_plato, name='agregar_plato'),
    path('plato/agregar_comida_plato/<int:pk>', views.agregar_comida_plato, name='agregar_comida_plato'),
    path('plato/eliminar/<int:pk>/', views.eliminar_plato, name='eliminar_plato'),
    path('plato/editar/<int:pk>/', views.editar_plato, name='editar_plato'),
    path('guardar_plato/<int:pk>/', views.guardar_plato, name='guardar_plato'),
    path('plato/<int:plato_id>/eliminar-comida/<int:comida_id>/', views.eliminar_comida_de_plato, name='eliminar_comida_de_plato'),

]