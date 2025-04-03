from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.urls import reverse
from django.utils.timezone import now
from datetime import datetime

from apps.pacientes.forms import AnalisisLabForm, AnamnesisForm, HistoriaClinicaForm, PacienteForm, ValorAntropometricoForm

# Formularios de tus modelos (ejemplo):


# Modelos:
from apps.pacientes.models import Paciente
from apps.comida.models import Plato
from apps.planNutricional.forms import PlanNutricionalForm
from .models import PlanNutricional, PlanDelDia

# ------------------------------------------------------------
# EJEMPLO DE LA VISTA para CREAR DATOS DEL PACIENTE
# (Botón "+"): obliga a cargar todos los formularios.
# ------------------------------------------------------------

from django.http import JsonResponse

def crear_datos_paciente(request, persona_id):
    """Crea (o guarda) en la BD la info de Obra Social, ValorAntropometrico, 
    AnalisisLab, Anamnesis, HistoriaClinica asociadas a un Paciente."""
    paciente = get_object_or_404(Paciente, persona_id=persona_id)

    if request.method == 'POST':
        # Instancia todos los formularios con la data del POST
        paciente_form = PacienteForm(request.POST, instance=paciente)
        antropometrico_form = ValorAntropometricoForm(request.POST)
        analisis_form = AnalisisLabForm(request.POST)
        anamnesis_form = AnamnesisForm(request.POST)
        historia_form = HistoriaClinicaForm(request.POST)

        # Verifica si TODOS son válidos
        if (paciente_form.is_valid() and
            antropometrico_form.is_valid() and
            analisis_form.is_valid() and
            anamnesis_form.is_valid() and
            historia_form.is_valid()):

            # Guarda los datos del paciente (ej. obra social) 
            paciente_form.save()

            # Guarda ValorAntropometrico
            val_antropo = antropometrico_form.save(commit=False)
            val_antropo.paciente = paciente
            val_antropo.save()

            # Guarda AnalisisLab
            analisis = analisis_form.save(commit=False)
            analisis.paciente = paciente
            analisis.save()

            # Guarda Anamnesis
            anam = anamnesis_form.save(commit=False)
            anam.paciente = paciente
            anam.save()

            # Guarda HistoriaClinica
            historia = historia_form.save(commit=False)
            historia.paciente = paciente
            historia.save()

            messages.success(request, "¡Datos del paciente creados exitosamente!")
            return redirect("pacientes:listapaciente")
        else:
            # Une todos los errores de los formularios
            error_messages = []
            for form in [paciente_form, antropometrico_form, analisis_form, anamnesis_form, historia_form]:
                if form.errors:
                    error_messages.extend(form.errors.values())
            
            messages.error(request, "Corrige los siguientes errores: " + " ".join([str(msg) for msg in error_messages]))
    else:
        # GET: formularios vacíos o inicializados si es que algo viene pre-cargado
        paciente_form = PacienteForm(instance=paciente)
        antropometrico_form = ValorAntropometricoForm()
        analisis_form = AnalisisLabForm()
        anamnesis_form = AnamnesisForm()
        historia_form = HistoriaClinicaForm()

    context = {
        'paciente': paciente,
        'paciente_form': paciente_form,
        'valor_antropometrico_form': antropometrico_form,
        'analisis_lab_form': analisis_form,
        'anamnesis_form': anamnesis_form,
        'historia_clinica_form': historia_form
    }
    return render(request, "pacientes/crear_datos_paciente.html", context)


# ------------------------------------------------------------
# VISTAS DEL PLAN NUTRICIONAL (tus funciones existentes)
# ------------------------------------------------------------
def crear_plan_nutricional(request, persona_id):
    paciente = get_object_or_404(Paciente, persona_id=persona_id)
    plan_existente = PlanNutricional.objects.filter(paciente=paciente).exists()

    if plan_existente:
        return redirect(f"{reverse('pacientes:listapaciente')}?plan_existente=1")

    if request.method == "POST":
        form = PlanNutricionalForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.paciente = paciente
            plan.save()
            messages.success(request, "Plan Nutricional creado exitosamente.")
            return redirect("pacientes:listapaciente")
    else:
        form = PlanNutricionalForm(initial={"paciente": paciente})

    return render(request, "plannutricional/plannutricional.html", {
        "form": form,
        "paciente": paciente,
    })


def crear_plan_dia(request, plan_nutricional_id):
    plan_nutricional = get_object_or_404(PlanNutricional, idPlanN=plan_nutricional_id)
    paciente = plan_nutricional.paciente

    if request.method == "POST":
        try:
            with transaction.atomic():
                for i in range(1, plan_nutricional.duracion_dias + 1):
                    for tipo in ['desayuno', 'almuerzo', 'merienda', 'cena']:
                        plato_ids = request.POST.getlist(f'plato_dia{i}_{tipo}')
                        descripcion = request.POST.get(f'descripcion_dia{i}_{tipo}')

                        if plato_ids:
                            plato_ids_int = [int(pid) for pid in plato_ids if pid.strip()]
                            plan_dia, created = PlanDelDia.objects.get_or_create(
                                plan_nutricional=plan_nutricional,
                                dia=i,
                                tipo_comida=tipo.upper(),
                                defaults={'descripcion': descripcion}
                            )
                            if not created and descripcion:
                                plan_dia.descripcion = descripcion
                            plan_dia.platos = plato_ids_int
                            plan_dia.save()

                messages.success(request, "Plan diario creado o actualizado exitosamente.")
                return redirect("pacientes:listapaciente")
        except Exception as e:
            messages.error(request, f"Error al crear o actualizar el plan diario: {str(e)}")
            return redirect("pacientes:listapaciente")

    platos = Plato.objects.all()
    rango_dias = range(1, plan_nutricional.duracion_dias + 1)
    planes_dia = PlanDelDia.objects.filter(plan_nutricional=plan_nutricional)

    return render(request, "plannutricional/plandiario.html", {
        "paciente": paciente,
        "platos": platos,
        "rango_dias": rango_dias,
        "tipo": "Plan",
        "planes_dia": planes_dia,
        "plan_nutricional": plan_nutricional
    })


def editar_plan_dia(request, plan_nutricional_id):
    plan_nutricional = get_object_or_404(PlanNutricional, idPlanN=plan_nutricional_id)
    paciente = plan_nutricional.paciente

    if request.method == "POST":
        try:
            with transaction.atomic():
                for i in range(1, plan_nutricional.duracion_dias + 1):
                    for tipo in ['desayuno', 'almuerzo', 'merienda', 'cena']:
                        plato_ids = request.POST.getlist(f'plato_dia{i}_{tipo}')
                        descripcion = request.POST.get(f'descripcion_dia{i}_{tipo}', '').strip()

                        plan_dia, created = PlanDelDia.objects.get_or_create(
                            plan_nutricional=plan_nutricional,
                            dia=i,
                            tipo_comida=tipo.upper(),
                            defaults={'descripcion': descripcion if descripcion else None,
                                      'platos': []}
                        )
                        plato_ids_int = [int(pid) for pid in plato_ids if pid.strip()] if plato_ids else []
                        plan_dia.platos = plato_ids_int
                        plan_dia.descripcion = descripcion if descripcion else None
                        plan_dia.save()

                messages.success(request, "Plan diario editado exitosamente.")
                return redirect("pacientes:listapaciente")
        except Exception as e:
            messages.error(request, f"Error al editar el plan diario: {str(e)}")
            return redirect("pacientes:listapaciente")

    platos = Plato.objects.all()
    rango_dias = range(1, plan_nutricional.duracion_dias + 1)
    planes_dia = PlanDelDia.objects.filter(plan_nutricional=plan_nutricional)

    return render(request, "plannutricional/plandiarioeditar.html", {
        "paciente": paciente,
        "platos": platos,
        "rango_dias": rango_dias,
        "tipo": "Plan",
        "planes_dia": planes_dia,
        "plan_nutricional": plan_nutricional
    })




def editar_paciente(request, persona_id):
    paciente = get_object_or_404(Paciente, persona_id=persona_id)
    
    if request.method == 'POST':
        paciente_form = PacienteForm(request.POST, instance=paciente)
        antropometrico_form = ValorAntropometricoForm(request.POST)
        analisis_form = AnalisisLabForm(request.POST)
        anamnesis_form = AnamnesisForm(request.POST)
        historia_form = HistoriaClinicaForm(request.POST)

        if (paciente_form.is_valid() and
            antropometrico_form.is_valid() and
            analisis_form.is_valid() and
            anamnesis_form.is_valid() and
            historia_form.is_valid()):
            
            paciente_form.save()
            val_antropo = antropometrico_form.save(commit=False)
            val_antropo.paciente = paciente
            val_antropo.save()

            analisis = analisis_form.save(commit=False)
            analisis.paciente = paciente
            analisis.save()

            anam = anamnesis_form.save(commit=False)
            anam.paciente = paciente
            anam.save()

            historia = historia_form.save(commit=False)
            historia.paciente = paciente
            historia.save()

            messages.success(request, "¡Datos del paciente editados exitosamente!")
            return redirect("pacientes:listapaciente")
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        paciente_form = PacienteForm(instance=paciente)
        antropometrico_form = ValorAntropometricoForm()
        analisis_form = AnalisisLabForm()
        anamnesis_form = AnamnesisForm()
        historia_form = HistoriaClinicaForm()

    context = {
        'paciente': paciente,
        'paciente_form': paciente_form,
        'valor_antropometrico_form': antropometrico_form,
        'analisis_lab_form': analisis_form,
        'anamnesis_form': anamnesis_form,
        'historia_clinica_form': historia_form
    }
    return render(request, "pacientes/editar_paciente.html", context)




def eliminar_plan_nutricional(request, plan_nutricional_id):
    plan = get_object_or_404(PlanNutricional, idPlanN=plan_nutricional_id)
    if request.method == "POST":
        plan.delete()
        messages.success(request, "Plan nutricional eliminado exitosamente.")
        return redirect("pacientes:listapaciente")

    return render(request, "plannutricional/confirm_delete.html", {"plan": plan})


def crear_plan_nutricional_modal(request, paciente_id):
    paciente = get_object_or_404(Paciente, persona_id=paciente_id)

    # Si el paciente ya tiene plan, opcionalmente podrías redirigir o mostrar mensaje de error
    if paciente.planes_nutricionales.exists():
        messages.warning(request, "Este paciente ya tiene un plan nutricional.")
        return redirect('pacientes:listapaciente')

    if request.method == 'POST':
        fecha_inicio_str = request.POST.get('fecha_inicio')
        duracion_dias_str = request.POST.get('duracion_dias')
        recomendacion = request.POST.get('recomendacion', '')

        if fecha_inicio_str:
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d')
        else:
            fecha_inicio = now()

        duracion_dias = int(duracion_dias_str) if duracion_dias_str else 30

        plan = PlanNutricional.objects.create(
            paciente=paciente,
            fecha_inicio=fecha_inicio,
            duracion_dias=duracion_dias,
            recomendacion=recomendacion,
            # nutricionista=request.user.nutricionista  # Si necesitas asociar a un nutricionista
        )

        messages.success(request, "Plan Nutricional creado exitosamente.")
        return redirect('plannutricional:crear_plan_dia', plan_nutricional_id=plan.idPlanN)

    return redirect('pacientes:listapaciente')
