from django.urls import path
from . import views

app_name = 'comida'

urlpatterns = [
    path("", views.comida, name='comida'),
    path('agregar_comida/', views.agregar_comida, name='agregar_comida'),
    path('plato/', views.plato, name='plato'),
]