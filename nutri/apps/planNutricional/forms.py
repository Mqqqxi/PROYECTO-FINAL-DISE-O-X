from django import forms
from .models import PlanDelDia, PlanNutricional

from django import forms
from .models import PlanDelDia

class PlanDelDiaForm(forms.ModelForm):
    class Meta:
        model = PlanDelDia
        fields = ["dia", "tipo_comida", "platos", "descripcion"]


class PlanNutricionalForm(forms.ModelForm):
    class Meta:
        model = PlanNutricional
        fields = ["duracion_dias", "fecha_inicio", "recomendacion"]