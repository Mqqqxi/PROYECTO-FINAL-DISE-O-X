from django import forms
from .models import PlanDelDia, PlanNutricional

class PlanDelDiaForm(forms.ModelForm):
    class Meta:
        model = PlanDelDia
        fields = ["dia", "tipo_comida", "plato1", "plato2", "plato3", "descripcion"]

class PlanNutricionalForm(forms.ModelForm):
    class Meta:
        model = PlanNutricional
        fields = ["duracion_dias", "fecha_inicio", "recomendacion"]