from django.contrib.auth.forms import UserCreationForm
from .models import Persona

from django import forms

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = Persona
        fields = ['email', 'first_name', 'last_name','telefono','direccion','fechaNacimiento', 'numDocumento', 'genero',  'tipoDocumento', 'password1', 'password2']

        def clean_numDocumento(self):
            numDocumento = self.cleaned_data['numDocumento']
            if not numDocumento.isdigit():
                raise forms.ValidationError('El número de documento solo puede contener números.')
            return numDocumento
