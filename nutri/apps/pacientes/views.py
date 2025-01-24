from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django import forms

from apps.persona.models import Persona

from .forms import RegistroPacienteForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from django.contrib import messages

# Vista para el registro de pacientes
def registro_paciente(request):
    if request.method == 'POST':
        form = RegistroPacienteForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Iniciar sesión automáticamente después del registro
            return redirect('inicio')  # Redirige a la página principal o donde prefieras
    else:
        form = RegistroPacienteForm()
    return render(request, 'pacientes/registro.html', {'form': form})

# Vista para el login
def login_paciente(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_paciente:  # Verificar que sea un paciente
                login(request, user)
                return redirect('inicio')  # Redirige a la página principal o donde prefieras
            else:
                form.add_error(None, 'Solo los pacientes pueden iniciar sesión.')
    else:
        form = AuthenticationForm()
    return render(request, 'pacientes/login.html', {'form': form})

# Formulario para editar el perfil del paciente
class PerfilPacienteForm(forms.ModelForm):
    # Campos del perfil
    class Meta:
        model = Persona
        fields = ['first_name', 'last_name', 'email', 'telefono', 'direccion', 'tipoDocumento', 'numDocumento']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'tipoDocumento': forms.TextInput(attrs={'class': 'form-control'}),
            'numDocumento': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CambiarContraseñaForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

def editar_perfil_paciente(request):
    if not request.user.is_paciente:
        return redirect('inicio')

    # Inicializar los formularios
    form = PerfilPacienteForm(instance=request.user)
    password_form = CambiarContraseñaForm(request.user)

    if request.method == 'POST':
        if 'guardar_perfil' in request.POST:
            form = PerfilPacienteForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, '¡Tu perfil se ha actualizado correctamente!')
                return redirect('pacientes:perfil')

        if 'cambiar_contraseña' in request.POST:
            password_form = CambiarContraseñaForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()  # Actualiza la contraseña
                update_session_auth_hash(request, user)  # Mantener la sesión activa
                messages.success(request, '¡Contraseña cambiada con éxito!')
                return redirect('pacientes:perfil')
            else:
                messages.error(request, 'Error al cambiar la contraseña. Verifica los datos ingresados.')

    contexto = {
        'form': form,
        'password_form': password_form
    }

    return render(request, 'pacientes/perfil.html', contexto)


def seguimiento_paciente(request):
    return render(request, 'pacientes/seguimiento.html')


def listapaciente(request):
    pacientes = Persona.objects.filter(is_paciente=True)
    return render(request, 'pacientes/listapaciente.html', {'pacientes': pacientes})