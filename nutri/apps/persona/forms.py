from django.contrib.auth.forms import UserCreationForm
from .models import Persona

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = Persona
        fields = ['email', 'first_name', 'last_name', 'fechaNacimiento', 'numDocumento', 'genero',  'tipoDocumento', 'password1', 'password2']
