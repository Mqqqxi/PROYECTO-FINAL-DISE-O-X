from django import forms
from .models import PlanDelDia, PlanNutricional

from datetime import date
from django.core.exceptions import ValidationError

class PlanDelDiaForm(forms.ModelForm):
    class Meta:
        model = PlanDelDia
        fields = ["dia", "tipo_comida", "plato1", "plato2", "plato3", "descripcion"]

class PlanNutricionalForm(forms.ModelForm):
    class Meta:
        model = PlanNutricional
        fields = ["duracion_dias", "fecha_inicio", "recomendacion"]
        widgets = {
            'fecha_inicio': forms.DateInput(
                attrs={
                    'type': 'date',
                    'min': date.today().isoformat(),  # Fecha mínima: hoy
                    'class': 'form-control',
                    'required': 'required',
                }
            ),
            'duracion_dias': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '1',
                    'value': '30',
                    'required': 'required',
                }
            ),
            'recomendacion': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'required': 'required',
                }
            ),
        }
    
    def clean_fecha_inicio(self):
        fecha_inicio = self.cleaned_data.get('fecha_inicio')
        if fecha_inicio and fecha_inicio < date.today():
            raise ValidationError("La fecha de inicio debe ser hoy o una fecha futura.")
        return fecha_inicio