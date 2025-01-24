from django import forms
from .models import Comida

class ComidaForm(forms.ModelForm):
    class Meta:
        model = Comida
        fields = [
            'nombre', 'imagen', 'calorias', 'colesterol', 'proteina', 
            'carbohidratos', 'grasaPolinsaturadas', 'grasaMoninsaturadas', 
            'grasaTrans', 'grasaTotales', 'grasaSaturadas', 'fibraAlimentaria', 
            'sodio', 'reqEnergetico','categoria'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la comida'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'calorias': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Calorías'}),
            'colesterol': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Colesterol'}),
            'proteina': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Proteínas'}),
            'carbohidratos': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Carbohidratos'}),
            'grasaPolinsaturadas': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Grasas poliinsaturadas'}),
            'grasaMoninsaturadas': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Grasas monoinsaturadas'}),
            'grasaTrans': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Grasas trans'}),
            'grasaTotales': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Grasas totales'}),
            'grasaSaturadas': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Grasas saturadas'}),
            'fibraAlimentaria': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Fibra alimentaria'}),
            'sodio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Sodio'}),
            'reqEnergetico': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Requerimiento energético'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Categoría'}),
        }