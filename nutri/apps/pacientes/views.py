from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.db.models import OuterRef, Subquery
from apps.turno.models import Turno
from .models import Paciente, ValorAntropometrico, AnalisisLab, Anamnesis, HistoriaClinica
from .forms import PacienteForm, ValorAntropometricoForm, AnalisisLabForm, AnamnesisForm, HistoriaClinicaForm
from apps.progreso.models import Progreso  # Ajusta según la ubicación real
from apps.persona.models import Persona
from apps.pacientes.models import Paciente

from .forms import RegistroPacienteForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from django.contrib import messages

def listapacientenuevo(request):
    pacientes = Paciente.objects.all()
    contexto = {
        'pacientes': pacientes  # Envolver el QuerySet en un diccionario
    }
    return render(request, 'pacientes/listapacientenuevo.html', contexto)


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


from django.shortcuts import get_object_or_404, render, redirect

from django.http import JsonResponse

def editar_paciente(request, persona_id):
    paciente = get_object_or_404(Paciente, persona_id=persona_id)

    valor_antropometrico = getattr(paciente, 'valores_antropometricos', None)
    analisis_lab = getattr(paciente, 'analisis_lab', None)
    anamnesis = getattr(paciente, 'anamnesis', None)
    historia_clinica = getattr(paciente, 'historia_clinica', None)

    if request.method == 'POST':
        paciente_form = PacienteForm(request.POST, instance=paciente)
        valor_antropometrico_form = ValorAntropometricoForm(request.POST, instance=valor_antropometrico)
        analisis_lab_form = AnalisisLabForm(request.POST, instance=analisis_lab)
        anamnesis_form = AnamnesisForm(request.POST, instance=anamnesis)
        historia_clinica_form = HistoriaClinicaForm(request.POST, instance=historia_clinica)

        # Verificar que todos los formularios sean válidos
        forms_validos = (paciente_form.is_valid() and
                         valor_antropometrico_form.is_valid() and
                         analisis_lab_form.is_valid() and
                         anamnesis_form.is_valid() and
                         historia_clinica_form.is_valid())

        if forms_validos:
            paciente_form.save()

            valor_antropometrico_instance = valor_antropometrico_form.save(commit=False)
            if not valor_antropometrico:
                valor_antropometrico_instance.paciente = paciente
            valor_antropometrico_form.save()

            analisis_lab_instance = analisis_lab_form.save(commit=False)
            if not analisis_lab:
                analisis_lab_instance.paciente = paciente
            analisis_lab_form.save()

            anamnesis_instance = anamnesis_form.save(commit=False)
            if not anamnesis:
                anamnesis_instance.paciente = paciente
            anamnesis_form.save()

            historia_clinica_instance = historia_clinica_form.save(commit=False)
            if not historia_clinica:
                historia_clinica_instance.paciente = paciente
            historia_clinica_form.save()

            # Si es una solicitud AJAX, devolvemos un JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            messages.success(request, "¡Todos los datos han sido guardados correctamente!")
            return redirect('pacientes:listapacientenuevo')
        else:
            # Si es una solicitud AJAX, devolvemos un JSON con error
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False})
            messages.error(request, "Por favor, corrige los errores en los campos.")

    else:
        paciente_form = PacienteForm(instance=paciente)
        valor_antropometrico_form = ValorAntropometricoForm(instance=valor_antropometrico)
        analisis_lab_form = AnalisisLabForm(instance=analisis_lab)
        anamnesis_form = AnamnesisForm(instance=anamnesis)
        historia_clinica_form = HistoriaClinicaForm(instance=historia_clinica)

    return render(request, 'pacientes/editar_perfil_paciente.html', {
        'paciente_form': paciente_form,
        'valor_antropometrico_form': valor_antropometrico_form,
        'analisis_lab_form': analisis_lab_form,
        'anamnesis_form': anamnesis_form,
        'historia_clinica_form': historia_clinica_form,
        'paciente': paciente,
    })

def deshabilitar_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    paciente.persona.is_active = not paciente.persona.is_active  # Alterna entre activo/inactivo
    paciente.persona.save()
    return redirect('pacientes:listapacientenuevo')


def habilitar_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    paciente.persona.is_active = True  # Activar al paciente
    paciente.persona.save()
    return redirect('pacientes:listapacientenuevo')

from django.http import JsonResponse

def crear_datos_paciente(request, persona_id):
    paciente = get_object_or_404(Paciente, persona_id=persona_id)

    if request.method == 'POST':
        paciente_form = PacienteForm(request.POST, instance=paciente)
        valor_antropometrico_form = ValorAntropometricoForm(request.POST)
        analisis_lab_form = AnalisisLabForm(request.POST)
        anamnesis_form = AnamnesisForm(request.POST)
        historia_clinica_form = HistoriaClinicaForm(request.POST)

        # Verificamos que TODOS los formularios sean válidos
        forms_validos = (paciente_form.is_valid() and
                         valor_antropometrico_form.is_valid() and
                         analisis_lab_form.is_valid() and
                         anamnesis_form.is_valid() and
                         historia_clinica_form.is_valid())

        if forms_validos:
            # Guardamos los datos
            paciente_form.save()  # Guarda obraSocial en Paciente

            valor_antropometrico_instance = valor_antropometrico_form.save(commit=False)
            valor_antropometrico_instance.paciente = paciente
            valor_antropometrico_instance.save()

            analisis_lab_instance = analisis_lab_form.save(commit=False)
            analisis_lab_instance.paciente = paciente
            analisis_lab_instance.save()

            anamnesis_instance = anamnesis_form.save(commit=False)
            anamnesis_instance.paciente = paciente
            anamnesis_instance.save()

            historia_clinica_instance = historia_clinica_form.save(commit=False)
            historia_clinica_instance.paciente = paciente
            historia_clinica_instance.save()

            # Si es una solicitud AJAX, devolvemos un JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            messages.success(request, "¡Todos los datos han sido guardados correctamente!")
            return redirect('pacientes:listapaciente')
        else:
            # Si es una solicitud AJAX, devolvemos un JSON con error
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False})
            messages.error(request, "Por favor, completa todos los campos en todas las secciones.")

    else:
        paciente_form = PacienteForm(instance=paciente)
        valor_antropometrico_form = ValorAntropometricoForm()
        analisis_lab_form = AnalisisLabForm()
        anamnesis_form = AnamnesisForm()
        historia_clinica_form = HistoriaClinicaForm()

    return render(request, 'pacientes/crear_datos_paciente.html', {
        'paciente_form': paciente_form,
        'valor_antropometrico_form': valor_antropometrico_form,
        'analisis_lab_form': analisis_lab_form,
        'anamnesis_form': anamnesis_form,
        'historia_clinica_form': historia_clinica_form,
        'paciente': paciente,
    })


def infopaciente(request, persona_id):
    # Obtener el paciente o devolver un error 404 si no existe
    paciente = get_object_or_404(Paciente, persona_id=persona_id)

    # Obtener los datos relacionados con el paciente
    valores_antropometricos = getattr(paciente, 'valores_antropometricos', None)
    analisis_lab = getattr(paciente, 'analisis_lab', None)
    anamnesis = getattr(paciente, 'anamnesis', None)
    historia_clinica = getattr(paciente, 'historia_clinica', None)

    # Obtener el peso más reciente de la tabla Progreso
    progreso_reciente = Progreso.objects.filter(paciente=paciente).order_by('-fecha').first()
    peso_actual = progreso_reciente.peso if progreso_reciente else None

    # Obtener la fecha actual en formato string
    fecha_actual = timezone.now().strftime('%Y-%m-%d')
    
    # Obtener todos los turnos del paciente
    turnos = Turno.objects.filter(paciente=paciente)
    
    # Filtrar próximos turnos
    proximos_turnos = turnos.filter(dia__gte=fecha_actual).order_by('dia', 'hora')
    proximo_turno = proximos_turnos.first() if proximos_turnos.exists() else None
    
    # Filtrar turnos pasados
    turnos_pasados = turnos.filter(dia__lt=fecha_actual).order_by('-dia', '-hora')
    ultimo_turno = turnos_pasados.first() if turnos_pasados.exists() else None

    # Calcular peso inicial, meta y diferencia
    peso_inicial = valores_antropometricos.peso if valores_antropometricos else None
    peso_meta = None  # Define esta lógica según tu modelo o requisitos
    diferencia_peso = None
    porcentaje_completado = None
    
    if peso_inicial and peso_actual and peso_meta:
        diferencia_peso = peso_actual - peso_inicial
        if peso_inicial != peso_meta:  # Evitar división por cero
            porcentaje_completado = ((peso_inicial - peso_actual) / (peso_inicial - peso_meta)) * 100

    # Contexto para el template
    contexto = {
        'paciente': paciente,
        'valores_antropometricos': valores_antropometricos,
        'analisis_lab': analisis_lab,
        'anamnesis': anamnesis,
        'historia_clinica': historia_clinica,
        'proximo_turno': proximo_turno,
        'ultimo_turno': ultimo_turno,
        'peso_inicial': peso_inicial,
        'peso_actual': peso_actual,  # Nuevo campo para peso actual
        'peso_meta': peso_meta,
        'diferencia_peso': diferencia_peso,
        'porcentaje_completado': porcentaje_completado,
    }

    return render(request, 'pacientes/infopaciente.html', contexto)