from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from apps.planNutricional.forms import PlanDelDiaForm, PlanNutricionalForm
from apps.comida.models import Comida, Plato, PlatoComida
from apps.pacientes.models import Paciente
from apps.persona.models import Nutricionista
from .models import PlanDelDia, PlanNutricional

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
            return redirect("pacientes:listapaciente")
    else:
        form = PlanNutricionalForm(initial={"paciente": paciente})

    return render(request, "plannutricional/plannutricional.html", {
        "form": form,
        "paciente": paciente,
    })


def crear_plan_dia(request, paciente_id):
    plan_nutricional = get_object_or_404(PlanNutricional, paciente_id=paciente_id)
    rango_dias = range(1, plan_nutricional.duracion_dias + 1)
    platos = Plato.objects.all()
    comidas = Comida.objects.all()
    tipo_comida = ["Desayuno", "Almuerzo", "Merienda", "Cena"]
    
    if request.method == "POST":
        # Process form submission
        for dia in rango_dias:
            for tipo in tipo_comida:
                tipo_lower = tipo.lower()
                
                # Process platos (dishes)
                plato_keys = [k for k in request.POST.keys() if k.startswith(f'plato_dia{dia}_{tipo_lower}')]
                for key in plato_keys:
                    plato_ids = request.POST.getlist(key)
                    for plato_id in plato_ids:
                        if plato_id:  # Check if not empty
                            try:
                                plato = get_object_or_404(Plato, idplato=plato_id)
                                
                                # Un plato puede tener múltiples comidas asociadas
                                # Tomamos el primer PlatoComida asociado a este plato
                                plato_comida = plato.platocomida_set.first()
                                
                                if plato_comida:
                                    # Crear PlanDelDia con este PlatoComida
                                    PlanDelDia.objects.create(
                                        plan_nutricional=plan_nutricional,
                                        dia=dia,
                                        tipo_comida=tipo.upper(),
                                        plato=plato_comida,
                                        descripcion=f"Plato: {plato.nombre}"
                                    )
                                else:
                                    # Si el plato no tiene comidas asociadas, no lo podemos usar
                                    messages.warning(
                                        request, 
                                        f"El plato '{plato.nombre}' no tiene comidas asociadas y no se puede agregar al plan."
                                    )
                            except Exception as e:
                                messages.warning(
                                    request, 
                                    f"Error al agregar el plato '{plato_id}': {str(e)}"
                                )
                
                # Process comidas (foods)
                comida_keys = [k for k in request.POST.keys() if k.startswith(f'comida_dia{dia}_{tipo_lower}')]
                for key in comida_keys:
                    comida_ids = request.POST.getlist(key)
                    for comida_id in comida_ids:
                        if comida_id:  # Check if not empty
                            try:
                                comida = get_object_or_404(Comida, idcomida=comida_id)
                                
                                # Para agregar solo una comida, necesitamos:
                                # 1. Crear un Plato temporal si no queremos reutilizar uno existente
                                # 2. Crear un PlatoComida que asocie el Plato con la Comida
                                temp_plato = Plato.objects.create(
                                    nombre=f"Comida Individual: {comida.nombre}",
                                    tipo=tipo_lower,
                                    descripcion=f"Plato generado automáticamente para la comida {comida.nombre}"
                                )
                                
                                # Ahora creamos el PlatoComida
                                plato_comida = PlatoComida.objects.create(
                                    plato=temp_plato,
                                    comida=comida,
                                    peso=100  # Peso por defecto en gramos
                                )
                                
                                # Finalmente creamos el PlanDelDia
                                PlanDelDia.objects.create(
                                    plan_nutricional=plan_nutricional,
                                    dia=dia,
                                    tipo_comida=tipo.upper(),
                                    plato=plato_comida,
                                    descripcion=f"Comida: {comida.nombre}"
                                )
                            except Exception as e:
                                messages.warning(
                                    request, 
                                    f"Error al agregar la comida '{comida_id}': {str(e)}"
                                )
        
        messages.success(request, "¡Plan Nutricional guardado exitosamente!")
        return redirect("pacientes:listapaciente")
    
    return render(request, "plannutricional/plandiario.html", {
        "plan_nutricional": plan_nutricional, 
        "rango_dias": rango_dias, 
        "platos": platos, 
        "comidas": comidas,
        "tipo_comida": tipo_comida,
    })