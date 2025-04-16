from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Persona, Paciente
from .models import Paciente, ValorAntropometrico, AnalisisLab, Anamnesis, HistoriaClinica
class RegistroPacienteForm(UserCreationForm):
    class Meta:
        model = Persona
        fields = ['email', 'first_name', 'last_name', 'fechaNacimiento', 'numDocumento', 'genero',  'tipoDocumento', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_paciente = True  # Marcar como paciente
        user.is_nutricionista = False
        if commit:
            user.save()
            # Crear el perfil de paciente asociado
            Paciente.objects.create(persona=user)
        return user

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['obraSocial']


class ValorAntropometricoForm(forms.ModelForm):
    class Meta:
        model = ValorAntropometrico
        fields = '__all__'
        exclude = ['paciente']

class AnalisisLabForm(forms.ModelForm):
    class Meta:
        model = AnalisisLab
        fields = '__all__'
        exclude = ['paciente']

class AnamnesisForm(forms.ModelForm):
    class Meta:
        model = Anamnesis
        exclude = ['paciente']

class HistoriaClinicaForm(forms.ModelForm):
    class Meta:
        model = HistoriaClinica
        exclude = ['paciente']
