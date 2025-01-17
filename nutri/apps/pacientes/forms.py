from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Persona, Paciente

class RegistroPacienteForm(UserCreationForm):
    class Meta:
        model = Persona
        fields = ['email', 'first_name', 'last_name', 'numDocumento', 'tipoDocumento', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_paciente = True  # Marcar como paciente
        user.is_nutricionista = False
        if commit:
            user.save()
            # Crear el perfil de paciente asociado
            Paciente.objects.create(persona=user)
        return user






# from django import forms
# from .models import Persona, Medico,Recepcionista,Enfermero
# from django.contrib.auth.forms import AuthenticationForm

# class CustomAuthenticationForm(AuthenticationForm):
#     username = forms.EmailField(label="Correo electrónico", widget=forms.EmailInput(attrs={'class': 'form-control'}))


# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from .models import Persona

# class CustomUserCreationForm(UserCreationForm):
#     usable_password = None
#     class Meta:
#         model = Persona
#         fields = ['first_name', 'last_name', 'email', 'dni', 'telefono', 'domicilio', 'genero', 'fecha_nacimiento']
#         labels = {
#             'first_name': 'Nombre',
#             'last_name': 'Apellido',
#             'email': 'Correo electrónico',
#             'dni': 'DNI',
#             'telefono': 'Teléfono',
#             'domicilio': 'Domicilio',
#             'genero': 'Género',
#             'fecha_nacimiento': 'Fecha de nacimiento',
#         }
# class CustomUserChangeForm(UserChangeForm):
#     class Meta:
#         model = Persona
#         fields = ['first_name', 'last_name', 'email', 'telefono', 'domicilio']
#         labels = {
#             'first_name': 'Nombre',
#             'last_name': 'Apellido',
#         }

# class MedicoForm(forms.ModelForm):
#     class Meta:
#         model = Medico
#         fields = ['especializacion', 'matricula']
        
# class EnfermeroForm(forms.ModelForm):
#     class Meta:
#         model = Enfermero
#         fields = ['matricula']
        
# class RecepcionistaForm(forms.ModelForm):
#     class Meta:
#         model = Recepcionista
#         fields = ['turno']