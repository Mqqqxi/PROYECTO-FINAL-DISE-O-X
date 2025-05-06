import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ComidaForm, PlatoForm
from .models import Comida, Plato, PlatoComida
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect


# Función para verificar si el usuario es nutricionista
def is_nutricionista(user):
    return user.is_nutricionista

# Función para verificar si el usuario es paciente
def is_paciente(user):
    return user.is_paciente



# Vista para ver todas las comidas
@login_required
##@user_passes_test(is_paciente)
# Create your views here.
def comida(request):
    comidas = Comida.objects.all()  # Obtén todas las comidas de la base de datos
    return render(request, 'comida/comida.html', {'comidas': comidas})

@login_required
@user_passes_test(is_nutricionista)
def agregar_comida(request):
    if request.method == 'POST':
        form = ComidaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('comida:comida')  # Redirige a la página de comida o donde desees
    else:
        form = ComidaForm()
    return render(request, 'comida/agregar_comida.html', {'form': form})

@user_passes_test(is_nutricionista)
def editar_comida(request, pk):
    comida = get_object_or_404(Comida, pk=pk)  # Obtener la comida por ID

    if request.method == 'POST':
        form = ComidaForm(request.POST, request.FILES, instance=comida)
        if form.is_valid():
            form.save()
            return redirect('comida:comida')  # Redirigir a la lista de comidas
    else:
        form = ComidaForm(instance=comida)

    return render(request, 'comida/editar_comida.html', {'form': form})

def eliminar_comida(request, pk):
    comida = get_object_or_404(Comida, pk=pk)

    if request.method == "POST":
        comida.delete()
        return JsonResponse({"success": True})
    
    return JsonResponse({"success": False, "error": "Método no permitido"}, status=400)



def plato(request):
    platos = Plato.objects.all()  # Obtén todas los platos de la base de datos
    return render(request, 'comida/plato.html', {'platos': platos})



def agregar_plato(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        tipo = request.POST.get('tipo')
        descripcion = request.POST.get('descripcion')

        if nombre and tipo:
            nuevo_plato = Plato.objects.create(
                nombre=nombre,
                tipo=tipo,
                descripcion=descripcion
            )
            return JsonResponse({"success": True, "plato_id": nuevo_plato.idplato})
        else:
            return JsonResponse({"success": False, "error": "Datos incompletos"}, status=400)
    
    return JsonResponse({"success": False, "error": "Método no permitido"}, status=400)


def eliminar_plato(request, pk):
    plato = get_object_or_404(Plato, pk=pk)

    if request.method == "POST":
        plato.delete()
        return JsonResponse({"success": True})
    
    return JsonResponse({"success": False, "error": "Método no permitido"}, status=400)


def editar_plato(request, pk):
    plato = get_object_or_404(Plato, pk=pk)  # Obtener la comida por ID

    if request.method == 'POST':
        form = PlatoForm(request.POST, request.FILES, instance=plato)
        if form.is_valid():
            form.save()
            return redirect('comida:plato')  # Redirigir a la lista de platos
    else:
        form = PlatoForm(instance=plato)

    return render(request, 'comida/editar_plato.html', {'form': form})



def agregar_comida_plato(request, pk):
    plato = get_object_or_404(Plato, pk=pk)  
    comidas = Comida.objects.all()
    comidasGuardadas= PlatoComida.objects.filter(plato=plato)

    return render(request, 'comida/platocomida.html', {'plato': plato, 'comidas': comidas, 'comidasGuardadas': comidasGuardadas})





@csrf_exempt
def guardar_plato(request, pk):
    if request.method == "POST":
        try:
            plato = get_object_or_404(Plato, pk=pk)
            comidas_seleccionadas = request.POST.get("comidas_seleccionadas")

            if not comidas_seleccionadas:
                return JsonResponse({"success": False, "error": "No se seleccionaron comidas"})

            comidas_ids = json.loads(comidas_seleccionadas)  

            # Recorrer los IDs de comidas y agregar solo las nuevas
            for comida_id in comidas_ids:
                comida = get_object_or_404(Comida, pk=comida_id)
                
                # Verificar si ya existe la relación antes de crearla
                if not PlatoComida.objects.filter(plato=plato, comida=comida).exists():
                    PlatoComida.objects.create(plato=plato, comida=comida, peso=100)

            return HttpResponseRedirect('/comida/plato')
            

        except Exception as e:
            # return JsonResponse({"success": False, "error": str(e)}, status=400)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    # return JsonResponse({"success": False, "error": "Método no permitido"}, status=400)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))






@csrf_exempt
def eliminar_comida_de_plato(request, plato_id, comida_id):
    if request.method == 'POST':
        try:
            # Buscar la relación específica
            plato_comida = PlatoComida.objects.filter(
                plato_id=plato_id,
                comida_id=comida_id
            ).first()
            
            if plato_comida:
                # Eliminar la relación
                plato_comida.delete()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({
                    'success': False, 
                    'error': 'No se encontró la relación plato-comida'
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
            
    return JsonResponse({
        'success': False,
        'error': 'Método no permitido'
    })


import logging

logger = logging.getLogger(__name__)

def obtener_comidas_plato(request, id_plato):
    try:
        relaciones = PlatoComida.objects.filter(plato_id=id_plato).select_related('comida')
        if not relaciones.exists():
            return JsonResponse({'comidas': []})
        comidas = []
        for relacion in relaciones:
            if relacion.comida.imagen:
                imagen_url = request.build_absolute_uri(relacion.comida.imagen.url)
            else:
                imagen_url = None  # O una URL de imagen por defecto
            
            comidas.append({
                'nombre': relacion.comida.nombre,
                'calorias': relacion.calorias_segun_peso(),
                'peso': relacion.peso,
                'imagen': imagen_url,  # Incluir la URL de la imagen
            })
        return JsonResponse({'comidas': comidas})
    except Exception as e:
        logger.error(f"Error al obtener comidas: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)
    






def actualizar_peso_plato_comida(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            plato_comida_id = data.get('id')
            nuevo_peso = data.get('peso')

            plato_comida = get_object_or_404(PlatoComida, id=plato_comida_id)
            plato_comida.peso = nuevo_peso
            plato_comida.save()

            return JsonResponse({
                'success': True,
                'calorias': plato_comida.calorias_segun_peso()
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=400)