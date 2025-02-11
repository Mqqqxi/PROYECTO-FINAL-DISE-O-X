from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.db.models import OuterRef, Subquery
from apps.turno.models import Turno
from .models import Paciente, ValorAntropometrico, AnalisisLab, Anamnesis, HistoriaClinica
from .forms import PacienteForm, ValorAntropometricoForm, AnalisisLabForm, AnamnesisForm, HistoriaClinicaForm
from apps.persona.models import Persona
from apps.pacientes.models import Paciente

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

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['obraSocial']


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


def lista_pacientes(request):
    pacientes = Persona.objects.filter(is_paciente=True).select_related('paciente', 'paciente__turno')
    return render(request, 'pacientes/listapaciente.html', {'pacientes': pacientes})


def editar_paciente(request, persona_id):
    paciente = get_object_or_404(Paciente, persona_id=persona_id)
    try:
        valor_antropometrico = paciente.valores_antropometricos
    except ValorAntropometrico.DoesNotExist:
        valor_antropometrico = None

    try:
        analisis_lab = paciente.analisis_lab
    except AnalisisLab.DoesNotExist:
        analisis_lab = None

    try:
        anamnesis = paciente.anamnesis
    except Anamnesis.DoesNotExist:
        anamnesis = None

    try:
        historia_clinica = paciente.historia_clinica
    except HistoriaClinica.DoesNotExist:
        historia_clinica = None
    
    if request.method == 'POST':
        paciente_form = PacienteForm(request.POST, instance=paciente)
        
        # Pasamos el paciente por defecto a los formularios correspondientes
        valor_antropometrico_form = ValorAntropometricoForm(request.POST, instance=valor_antropometrico)
        if valor_antropometrico_form.instance:
            valor_antropometrico_form.instance.paciente = paciente

        analisis_lab_form = AnalisisLabForm(request.POST, instance=analisis_lab)
        if analisis_lab_form.instance:
            analisis_lab_form.instance.paciente = paciente

        anamnesis_form = AnamnesisForm(request.POST, instance=anamnesis)
        if anamnesis_form.instance:
            anamnesis_form.instance.paciente = paciente

        historia_clinica_form = HistoriaClinicaForm(request.POST, instance=historia_clinica)
        if historia_clinica_form.instance:
            historia_clinica_form.instance.paciente = paciente

        if all([paciente_form.is_valid(), valor_antropometrico_form.is_valid(), 
                analisis_lab_form.is_valid(), anamnesis_form.is_valid(), historia_clinica_form.is_valid()]):

            paciente_form.save()
            valor_antropometrico_form.save()
            analisis_lab_form.save()
            anamnesis_form.save()
            historia_clinica_form.save()
            
            return redirect('pacientes:listapaciente')  # Redirigir a la lista de pacientes después de guardar
        else:
            print("Errores en los formularios:")
            print(paciente_form.errors)
            print(valor_antropometrico_form.errors)
            print(analisis_lab_form.errors)
            print(anamnesis_form.errors)
            print(historia_clinica_form.errors)
    else:
        paciente_form = PacienteForm(instance=paciente)
        
        # Asignar el paciente por defecto en la carga inicial de los formularios
        valor_antropometrico_form = ValorAntropometricoForm(instance=valor_antropometrico)
        if valor_antropometrico_form.instance:
            valor_antropometrico_form.instance.paciente = paciente

        analisis_lab_form = AnalisisLabForm(instance=analisis_lab)
        if analisis_lab_form.instance:
            analisis_lab_form.instance.paciente = paciente

        anamnesis_form = AnamnesisForm(instance=anamnesis)
        if anamnesis_form.instance:
            anamnesis_form.instance.paciente = paciente

        historia_clinica_form = HistoriaClinicaForm(instance=historia_clinica)
        if historia_clinica_form.instance:
            historia_clinica_form.instance.paciente = paciente

    return render(request, 'pacientes/editar_perfil_paciente.html', {
        'paciente_form': paciente_form,
        'valor_antropometrico_form': valor_antropometrico_form,
        'analisis_lab_form': analisis_lab_form,
        'anamnesis_form': anamnesis_form,
        'historia_clinica_form': historia_clinica_form,
    })

def deshabilitar_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    paciente.persona.is_active = not paciente.persona.is_active  # Alterna entre activo/inactivo
    paciente.persona.save()
    return redirect('pacientes:listapaciente')


def habilitar_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    paciente.persona.is_active = True  # Activar al paciente
    paciente.persona.save()
    return redirect('pacientes:listapaciente')