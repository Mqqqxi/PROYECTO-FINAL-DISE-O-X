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



def editar_plan_dia(request, paciente_id):
    paciente = get_object_or_404(Paciente, persona_id=paciente_id)
    plan_nutricional = get_object_or_404(PlanNutricional, paciente=paciente)
    
    if request.method == "POST":
        try:
            with transaction.atomic():
                platos_validos = set(Plato.objects.values_list('idplato', flat=True))
                for i in range(1, plan_nutricional.duracion_dias + 1):
                    for tipo in ['desayuno', 'almuerzo', 'merienda', 'cena']:
                        plato_ids = request.POST.getlist(f'plato_dia{i}_{tipo}')
                        descripcion = request.POST.get(f'descripcion_dia{i}_{tipo}')
                    
                        plato_ids_int = [int(pid) for pid in plato_ids if pid.strip() and int(pid) in platos_validos]
                    
                        # Usar get_or_create para actualizar en lugar de eliminar
                        plan_dia, created = PlanDelDia.objects.get_or_create(
                            plan_nutricional=plan_nutricional,
                            dia=i,
                            tipo_comida=tipo.upper(),
                            defaults={'descripcion': descripcion, 'platos': plato_ids_int}
                        )
                        if not created:
                            if plato_ids_int or descripcion:  # Actualiza si hay datos
                                plan_dia.platos = plato_ids_int
                                plan_dia.descripcion = descripcion
                                plan_dia.save()
                            elif not plato_ids_int and not descripcion:  # Elimina si no hay datos
                                plan_dia.delete()
            
                messages.success(request, "Plan diario actualizado exitosamente.")
                return redirect("pacientes:listapaciente")
        except Exception as e:
            messages.error(request, f"Error al actualizar el plan diario: {str(e)}")
            return redirect("pacientes:listapaciente")
    
    # GET: obtener todos los platos y los días del plan
    platos = Plato.objects.all()  
    rango_dias = range(1, plan_nutricional.duracion_dias + 1)
    planes_dia = PlanDelDia.objects.filter(plan_nutricional=plan_nutricional).select_related('plan_nutricional')
    
    # Diccionario para mapear IDs de platos a nombres (definido antes de usarlo)
    platos_dict = {plato.idplato: plato.nombre for plato in platos}

    # Armar estructuras para pasar a la plantilla
    planes_data_ids = {}  # Para IDs
    planes_data_nombres = {}  # Para nombres
    descripciones_data = {}
    for plan in planes_dia:
        clave_plato = f"plato_dia{plan.dia}_{plan.tipo_comida.lower()}"
        clave_desc = f"descripcion_dia{plan.dia}_{plan.tipo_comida.lower()}"
        planes_data_ids[clave_plato] = plan.platos  # Lista de IDs de platos
        planes_data_nombres[clave_plato] = [platos_dict[plato_id] for plato_id in plan.platos if plato_id in platos_dict]
        descripciones_data[clave_desc] = plan.descripcion or ""

    return render(request, "plannutricional/editarplandia.html", {
        "paciente": paciente,
        "platos": platos,
        "rango_dias": rango_dias,
        "tipo": "Editar Plan",
        "planes_data_ids": planes_data_ids,  # IDs para el input
        "planes_data_nombres": planes_data_nombres,  # Nombres para mostrar
        "descripciones_data": descripciones_data,
        "platos_dict": platos_dict,
        "plan_nutricional": plan_nutricional
    })

def crear_plan_dia(request, paciente_id):
    paciente = get_object_or_404(Paciente, persona_id=paciente_id)
    plan_nutricional = get_object_or_404(PlanNutricional, paciente=paciente)

    if request.method == "POST":
        try:
            with transaction.atomic():
                for i in range(1, plan_nutricional.duracion_dias + 1):
                    for tipo in ['desayuno', 'almuerzo', 'merienda', 'cena']:
                        plato_ids = request.POST.getlist(f'plato_dia{i}_{tipo}')  # Usamos getlist para obtener múltiples platos
                        descripcion = request.POST.get(f'descripcion_dia{i}_{tipo}')
                        
                        # In crear_plan_dia view
                        if plato_ids:  # Solo crear si se enviaron platos
    # Obtenemos los platos IDs como enteros
                            plato_ids_int = [int(pid) for pid in plato_ids if pid.strip()]
    
    # Creamos o actualizamos el PlanDelDia
                            plan_dia, created = PlanDelDia.objects.get_or_create(
                            plan_nutricional=plan_nutricional,
                            dia=i,
                            tipo_comida=tipo.upper(),
                             defaults={'descripcion': descripcion}
                            )
    
                            # Actualizamos descripción si no es un nuevo registro
                            if not created and descripcion:
                                plan_dia.descripcion = descripcion
    
    # Guardamos los IDs directamente
                            plan_dia.platos = plato_ids_int
                            plan_dia.save()
                            
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
        planes_data[clave] = plan.platos  # Ahora guardamos la lista de platos

    return render(request, "plannutricional/plandiario.html", {
        "paciente": paciente,
        "platos": platos,
        "rango_dias": rango_dias,
        "tipo": "Plan",
        "planes_data": planes_data,
        "plan_nutricional": plan_nutricional
    })