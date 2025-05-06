from django import forms
from .models import Comida, Plato

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
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
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

    def clean_nombre(self):
            nombre = self.cleaned_data.get('nombre')
            if any(char.isdigit() for char in nombre):
                raise forms.ValidationError("El nombre no debe contener números.")
            return nombre

    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')
        if not imagen:
            raise forms.ValidationError("Este campo es obligatorio.")
        return imagen


class PlatoForm(forms.ModelForm):
    class Meta:
        model = Plato
        fields = ['nombre', 'tipo', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del plato'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción del plato', 'rows': 3}),
        }

    def clean_nombre(self):
            nombre = self.cleaned_data.get('nombre')
            if any(char.isdigit() for char in nombre):
                raise forms.ValidationError("El nombre no debe contener números.")
            return nombre