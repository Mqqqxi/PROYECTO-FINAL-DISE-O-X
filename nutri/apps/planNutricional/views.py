from gettext import translation
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from apps.planNutricional.forms import PlanDelDiaForm, PlanNutricionalForm
from apps.comida.models import Comida, Plato, PlatoComida
from apps.pacientes.models import Paciente
from apps.persona.models import Nutricionista
from .models import PlanDelDia, PlanNutricional

from django.db import transaction

from django.urls import reverse

def crear_plan_nutricional(request, persona_id):
    paciente = get_object_or_404(Paciente, persona_id=persona_id)
    plan_existente = PlanNutricional.objects.filter(paciente=paciente).exists()

    if plan_existente:
        # Redirige al listado con un parámetro en la URL
        return redirect(f"{reverse('pacientes:listapaciente')}?plan_existente=1")

    if request.method == "POST":
        form = PlanNutricionalForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.paciente = paciente
            plan.save()
            # También puedes usar messages si lo prefieres
            messages.success(request, "Plan Nutricional creado exitosamente.")
            return redirect("pacientes:listapaciente")
    else:
        form = PlanNutricionalForm(initial={"paciente": paciente})

    return render(request, "plannutricional/plannutricional.html", {
        "form": form,
        "paciente": paciente,
    })

def crear_plan_dia(request, paciente_id):
    paciente = get_object_or_404(Paciente, persona_id=paciente_id)
    plan_nutricional = get_object_or_404(PlanNutricional, paciente=paciente)

    if request.method == "POST":
        try:
            with transaction.atomic():
                for i in range(1, plan_nutricional.duracion_dias + 1):
                    for tipo in ['desayuno', 'almuerzo', 'merienda', 'cena']:
                        plato_id = request.POST.get(f'plato_dia{i}_{tipo}')
                        descripcion = request.POST.get(f'descripcion_dia{i}_{tipo}')  # Esto ahora coincide con el HTML
                        if plato_id:  # Solo crear si se envió un plato
                            plato = get_object_or_404(Plato, idplato=plato_id)
                            PlanDelDia.objects.create(
                                plan_nutricional=plan_nutricional,
                                dia=i,
                                tipo_comida=tipo.upper(),
                                plato=plato,
                                descripcion=descripcion  # Esto debería funcionar ahora
                            )
                messages.success(request, "Plan diario creado exitosamente con nuevas filas.")
                return redirect("pacientes:listapaciente")
        except Exception as e:
            messages.error(request, f"Error al crear el plan diario: {str(e)}")
            return redirect("pacientes:listapaciente")

    # Código para GET permanece igual
    platos = Plato.objects.all()
    rango_dias = range(1, plan_nutricional.duracion_dias + 1)
    planes_dia = PlanDelDia.objects.filter(plan_nutricional=plan_nutricional)

    planes_data = {}
    for plan in planes_dia:
        clave = f"plato_dia{plan.dia}_{plan.tipo_comida.lower()}"
        planes_data[clave] = plan.plato.idplato

    return render(request, "plannutricional/plandiario.html", {
        "paciente": paciente,
        "platos": platos,
        "rango_dias": rango_dias,
        "tipo": "Plan",
        "planes_data": planes_data,
        "plan_nutricional": plan_nutricional
    })
