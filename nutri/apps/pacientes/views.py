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
from apps.planNutricional.models import PlanDelDia
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import RegistroPacienteForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from django.contrib import messages

from django.core.exceptions import ValidationError


# Función para verificar si el usuario es nutricionista
def is_nutricionista(user):
    return user.is_nutricionista

# Función para verificar si el usuario es paciente
def is_paciente(user):
    return user.is_paciente



from django.contrib.auth.decorators import login_required, user_passes_test

@login_required
@user_passes_test(is_nutricionista)
def listapacientenuevo(request):
    pacientes = Paciente.objects.all()
    contexto = {
        'pacientes': pacientes
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
            if user.is_paciente or user.is_nutricionista:  # Verificar que sea un paciente o nutricionista
                login(request, user)
                return redirect('inicio')  # Redirige a la página principal o donde prefieras
            else:
                form.add_error(None, 'Acceso denegado. No eres un paciente.')
    else:
        form = AuthenticationForm()
    return render(request, 'pacientes/login.html', {'form': form})

# Formulario para editar el perfil del paciente
class PerfilPacienteForm(forms.ModelForm):
    # Campos del perfil
    class Meta:
        model = Persona
        fields = ['first_name', 'last_name','genero', 'email', 'telefono', 'direccion', 'tipoDocumento', 'numDocumento']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': True}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'tipoDocumento': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),  # No editable
            'numDocumento': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),  # No editable
            'genero': forms.Select(
                attrs={'class': 'form-control selectpicker', 'required': True},
                choices=[('M', 'Masculino'), ('F', 'Femenino'), ('ND', 'No Definido')],
            ),
        }

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not telefono.isdigit() or len(telefono) != 10:
            raise ValidationError("El teléfono debe contener exactamente 10 dígitos numéricos.")
        return telefono

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name.isdigit():
            raise ValidationError("El nombre no puede ser numérico.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name.isdigit():
            raise ValidationError("El apellido no puede ser numérico.")
        return last_name

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['obraSocial', 'objetivo']


class CambiarContraseñaForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

# def editar_perfil_paciente(request):
#     # if not request.user.is_paciente:
#     #     return redirect('inicio')

#     # Inicializar los formularios
#     form = PerfilPacienteForm(instance=request.user)
#     password_form = CambiarContraseñaForm(request.user)

#     if request.method == 'POST':
#         if 'guardar_perfil' in request.POST:
#             form = PerfilPacienteForm(request.POST, instance=request.user)
#             if form.is_valid():
#                 form.save()
#                 messages.success(request, '¡Tu perfil se ha actualizado correctamente!')
#                 return redirect('pacientes:perfil')

#         if 'cambiar_contraseña' in request.POST:
#             password_form = CambiarContraseñaForm(request.user, request.POST)
#             if password_form.is_valid():
#                 user = password_form.save()  # Actualiza la contraseña
#                 update_session_auth_hash(request, user)  # Mantener la sesión activa
#                 messages.success(request, '¡Contraseña cambiada con éxito!')
#                 return redirect('pacientes:perfil')
#             else:
#                 messages.error(request, 'Error al cambiar la contraseña. Verifica los datos ingresados.')

#     contexto = {
#         'form': form,
#         'password_form': password_form
#     }

#     return render(request, 'pacientes/perfil.html', contexto)

def editar_perfil_paciente(request):
    form = PerfilPacienteForm(instance=request.user)
    password_form = CambiarContraseñaForm(request.user)

    if request.method == 'POST':
        if 'guardar_perfil' in request.POST:
            form = PerfilPacienteForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, '¡Tu perfil se ha actualizado correctamente!')
                return redirect('pacientes:perfil')  # ✅ <- Este return evita procesar el otro formulario

        elif 'cambiar_contraseña' in request.POST:
            password_form = CambiarContraseñaForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, '¡Contraseña cambiada con éxito!')
                return redirect('pacientes:perfil')
            else:
                messages.error(request, 'Error al cambiar la contraseña. Verifica los datos ingresados.')

    contexto = {
        'form': form,
        'password_form': password_form
    }

    return render(request, 'pacientes/perfil.html', contexto)



def mi_seguimiento(request, persona_id):
    # Obtener el paciente
    paciente = get_object_or_404(Paciente, persona_id=persona_id)
    return render(request, 'pacientes/infopaciente.html')


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
            return redirect('pacientes:listapacientenuevo')
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

from django.db import transaction
from django.urls import reverse
from django.utils import timezone
from apps.planNutricional.models import PlanNutricional, PlanDelDia
from apps.comida.models import Plato, Comida

from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from apps.planNutricional.models import PlanNutricional, PlanDelDia


from datetime import timedelta
from django.http import HttpResponseForbidden

@login_required
def infopaciente(request, paciente_id=None):
    """
    * paciente_id == None  ➜ el usuario autenticado debe ser paciente
    * paciente_id != None  ➜ el usuario autenticado debe ser nutricionista
    """
    if paciente_id is None:
        try:
            paciente = Paciente.objects.get(persona=request.user)
        except Paciente.DoesNotExist:
            return redirect("inicio")
    else:
        if not request.user.is_nutricionista:
            return HttpResponseForbidden("No tienes permiso para ver esto")
        paciente = get_object_or_404(Paciente, pk=paciente_id)
    
    valores_antropometricos = getattr(paciente, 'valores_antropometricos', None)
    analisis_lab = getattr(paciente, 'analisis_lab', None)
    anamnesis = getattr(paciente, 'anamnesis', None)
    historia_clinica = getattr(paciente, 'historia_clinica', None)

    progresos = Progreso.objects.filter(paciente=paciente).order_by('fecha')
    progreso_reciente = progresos.last()
    peso_actual = progreso_reciente.peso if progreso_reciente else None
    ultima_visita = progreso_reciente.fecha if progreso_reciente else None

    fecha_actual = timezone.now().date()
    turnos = Turno.objects.filter(paciente=paciente)
    proximos_turnos = turnos.filter(dia__gte=fecha_actual).order_by('dia', 'hora')
    proximo_turno = proximos_turnos.first() if proximos_turnos.exists() else None
    turnos_pasados = turnos.filter(dia__lt=fecha_actual).order_by('-dia', '-hora')
    ultimo_turno = turnos_pasados.first() if turnos_pasados.exists() else None

    peso_inicial = float(valores_antropometricos.peso) if valores_antropometricos and valores_antropometricos.peso is not None else None
    peso_meta = float(valores_antropometricos.peso_meta) if valores_antropometricos and hasattr(valores_antropometricos, 'peso_meta') and valores_antropometricos.peso_meta is not None else None
    diferencia_peso = peso_actual - peso_inicial if peso_actual is not None and peso_inicial is not None else None
    porcentaje_completado = None
    if peso_inicial is not None and peso_actual is not None and peso_meta is not None and peso_inicial != peso_meta:
        try:
            porcentaje_completado = ((peso_inicial - peso_actual) / (peso_inicial - peso_meta)) * 100
        except ZeroDivisionError:
            porcentaje_completado = None
    
    plan_nutricional = paciente.planes_nutricionales.first()
    if plan_nutricional:
        recomendacion = plan_nutricional.recomendacion
    else:
        recomendacion = None
    plan_data = []
    if plan_nutricional:
        dias = list(range(1, plan_nutricional.duracion_dias + 1))
        fecha_inicio = plan_nutricional.fecha_inicio.date()
        for dia in dias:
            planes_dia = PlanDelDia.objects.filter(plan_nutricional=plan_nutricional, dia=dia)
            desayuno = planes_dia.filter(tipo_comida="DESAYUNO").first()
            almuerzo = planes_dia.filter(tipo_comida="ALMUERZO").first()
            merienda = planes_dia.filter(tipo_comida="MERIENDA").first()
            cena = planes_dia.filter(tipo_comida="CENA").first()

            fecha_actual = fecha_inicio + timedelta(days=dia-1)

            def obtener_nombres(opciones):
                if not opciones:
                    return []
                return [item.get("nombre", "") for item in opciones]

            dia_nombre = fecha_actual.strftime("%d/%m/%Y")
            plan_data.append({
                'dia': dia,
                'dia_nombre': dia_nombre,
                'desayuno': {
                    'op1': obtener_nombres(desayuno.plato1) if desayuno else [],
                    'op2': obtener_nombres(desayuno.plato2) if desayuno else [],
                    'op3': obtener_nombres(desayuno.plato3) if desayuno else [],
                    'descripcion': desayuno.descripcion if desayuno and desayuno.descripcion else ''
                },
                'almuerzo': {
                    'op1': obtener_nombres(almuerzo.plato1) if almuerzo else [],
                    'op2': obtener_nombres(almuerzo.plato2) if almuerzo else [],
                    'op3': obtener_nombres(almuerzo.plato3) if almuerzo else [],
                    'descripcion': almuerzo.descripcion if almuerzo and almuerzo.descripcion else ''
                },
                'merienda': {
                    'op1': obtener_nombres(merienda.plato1) if merienda else [],
                    'op2': obtener_nombres(merienda.plato2) if merienda else [],
                    'op3': obtener_nombres(merienda.plato3) if merienda else [],
                    'descripcion': merienda.descripcion if merienda and merienda.descripcion else ''
                },
                'cena': {
                    'op1': obtener_nombres(cena.plato1) if cena else [],
                    'op2': obtener_nombres(cena.plato2) if cena else [],
                    'op3': obtener_nombres(cena.plato3) if cena else [],
                    'descripcion': cena.descripcion if cena and cena.descripcion else ''
                }
            })

    contexto = {
        'paciente': paciente,
        'valores_antropometricos': valores_antropometricos,
        'analisis_lab': analisis_lab,
        'anamnesis': anamnesis,
        'historia_clinica': historia_clinica,
        'progresos': progresos,
        'proximo_turno': proximo_turno,
        'ultimo_turno': ultimo_turno,
        'ultima_visita': ultima_visita,
        'peso_inicial': peso_inicial,
        'peso_actual': peso_actual,
        'peso_meta': peso_meta,
        'diferencia_peso': diferencia_peso,
        'porcentaje_completado': porcentaje_completado,
        'plan_data': plan_data,
        'recomendación' : recomendacion,
        'comidas_loop': ['desayuno', 'almuerzo', 'merienda', 'cena'],
        'today': timezone.now(),
        'is_nutricionista': request.user.is_nutricionista,  # Añadido explícitamente
    }
    return render(request, 'pacientes/infopaciente.html', contexto)