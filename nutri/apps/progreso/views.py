import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Progreso, FotoProgreso
from apps.pacientes.models import Paciente
from apps.persona.models import Nutricionista
from django.utils import timezone
from django.http import JsonResponse

import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Progreso, FotoProgreso
from apps.pacientes.models import Paciente
from apps.persona.models import Nutricionista
from django.utils import timezone
from django.http import JsonResponse

from datetime import date

@login_required
def CrearProgreso(request, paciente_pk):
    paciente = get_object_or_404(Paciente, pk=paciente_pk)
    progresos = Progreso.objects.filter(paciente=paciente).order_by('-fecha')

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        # Obtener la única nutricionista
        try:
            nutricionista = Nutricionista.objects.get()
        except Nutricionista.DoesNotExist:
            messages.error(request, 'No hay una nutricionista registrada.')
            return redirect('pacientes:infopaciente', persona_id=paciente.persona_id)

        # Formulario de evolución
        if form_type == 'evolucion':
            try:
                progreso = Progreso(
                    paciente=paciente,
                    nutricionista=nutricionista,  # Asignar la nutricionista
                    fecha=request.POST.get('fecha'),
                    peso=float(request.POST.get('peso')) if request.POST.get('peso') else 0.0,
                    comentario=request.POST.get('comentario', ''),
                    indice_grasa_corporal=float(request.POST.get('indice_grasa_corporal')) if request.POST.get('indice_grasa_corporal') else None,
                    perimetro_cintura=float(request.POST.get('perimetro_cintura')) if request.POST.get('perimetro_cintura') else None,
                    perimetro_cadera=float(request.POST.get('perimetro_cadera')) if request.POST.get('perimetro_cadera') else None,
                    perimetro_muslo=float(request.POST.get('perimetro_muslo')) if request.POST.get('perimetro_muslo') else None,
                    perimetro_brazo=float(request.POST.get('perimetro_brazo')) if request.POST.get('perimetro_brazo') else None,
                    perimetro_pecho=float(request.POST.get('perimetro_pecho')) if request.POST.get('perimetro_pecho') else None,
                    masa_muscular=float(request.POST.get('masa_muscular')) if request.POST.get('masa_muscular') else None,
                    agua_corporal=float(request.POST.get('agua_corporal')) if request.POST.get('agua_corporal') else None,
                    tension_arterial_maxima=float(request.POST.get('tension_arterial_maxima')) if request.POST.get('tension_arterial_maxima') else None,
                    tension_arterial_minima=float(request.POST.get('tension_arterial_minima')) if request.POST.get('tension_arterial_minima') else None,
                )
                progreso.save()
                messages.success(request, 'Datos de evolución guardados exitosamente')
                return redirect('pacientes:infopaciente', persona_id=paciente.persona_id)
            except ValueError as e:
                messages.error(request, f'Error en los datos numéricos: {str(e)}')
            except Exception as e:
                messages.error(request, f'Error al guardar evolución: {str(e)}')

        # Formulario de fotos
        elif form_type == 'fotos':
            try:
                progreso, created = Progreso.objects.get_or_create(
                    paciente=paciente,
                    nutricionista=nutricionista,  # Asignar la nutricionista
                    fecha=request.POST.get('fecha', timezone.now().date()),
                    defaults={'peso': 0.0}
                )
                fotos = [
                    ('foto_espalda', 'Espalda'),
                    ('foto_lado', 'Lado'),
                    ('foto_frente', 'Frente')
                ]
                for foto_field, descripcion in fotos:
                    if foto_field in request.FILES:
                        foto = FotoProgreso(
                            progreso=progreso,
                            foto=request.FILES[foto_field],
                            descripcion=descripcion,
                            creado=timezone.now()
                        )
                        foto.save()
                messages.success(request, 'Fotos guardadas exitosamente')
                return redirect('pacientes:infopaciente', persona_id=paciente.persona_id)
            except Exception as e:
                messages.error(request, f'Error al guardar fotos: {str(e)}')

    fechas = progresos.values_list('fecha', flat=True).distinct()

    context = {
        'paciente': paciente,
        'fechas': fechas,
        'progresos': progresos,
    }
    # return render(request, 'pacientes/infopaciente.html', context)
    return redirect('pacientes:infopaciente_detalle', paciente_id=paciente.pk)

# Configurar un logger
logger = logging.getLogger(__name__)

def obtener_datos_progreso(request, paciente_pk, fecha):
    paciente = get_object_or_404(Paciente, pk=paciente_pk)
    try:
        progreso = Progreso.objects.get(paciente=paciente, fecha=fecha)
        fotos = FotoProgreso.objects.filter(progreso=progreso)
        data = {
            'peso': progreso.peso,
            'indice_grasa_corporal': progreso.indice_grasa_corporal,
            'perimetro_cintura': progreso.perimetro_cintura,
            'perimetro_cadera': progreso.perimetro_cadera,
            'perimetro_muslo': progreso.perimetro_muslo,
            'perimetro_brazo': progreso.perimetro_brazo,
            'perimetro_pecho': progreso.perimetro_pecho,
            'masa_muscular': progreso.masa_muscular,
            'agua_corporal': progreso.agua_corporal,
            'tension_arterial_maxima': progreso.tension_arterial_maxima,
            'tension_arterial_minima': progreso.tension_arterial_minima,
            'comentario': progreso.comentario,
            'fotos': [{'url': foto.foto.url, 'descripcion': foto.descripcion} for foto in fotos]
        }
        return JsonResponse(data)
    except Progreso.DoesNotExist:
        logger.error(f"No se encontró Progreso para paciente {paciente_pk} en fecha {fecha}")
        return JsonResponse({'error': 'No se encontraron datos para la fecha seleccionada'}, status=404)
    except Exception as e:
        logger.error(f"Error en obtener_datos_progreso: {str(e)}", exc_info=True)
        return JsonResponse({'error': f'Error interno del servidor: {str(e)}'}, status=500)

def editar_progreso(request, paciente_pk):
    paciente = get_object_or_404(Paciente, pk=paciente_pk)
    
    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        if not fecha:
            messages.error(request, 'La fecha no fue proporcionada.')
            return redirect('pacientes:infopaciente', persona_id=paciente.persona_id)
        
        try:
            progreso = Progreso.objects.get(paciente=paciente, fecha=fecha)
            progreso.peso = float(request.POST.get('peso')) if request.POST.get('peso') else 0.0
            progreso.indice_grasa_corporal = float(request.POST.get('indice_grasa_corporal')) if request.POST.get('indice_grasa_corporal') else None
            progreso.perimetro_cintura = float(request.POST.get('perimetro_cintura')) if request.POST.get('perimetro_cintura') else None
            progreso.perimetro_cadera = float(request.POST.get('perimetro_cadera')) if request.POST.get('perimetro_cadera') else None
            progreso.perimetro_muslo = float(request.POST.get('perimetro_muslo')) if request.POST.get('perimetro_muslo') else None
            progreso.perimetro_brazo = float(request.POST.get('perimetro_brazo')) if request.POST.get('perimetro_brazo') else None
            progreso.perimetro_pecho = float(request.POST.get('perimetro_pecho')) if request.POST.get('perimetro_pecho') else None
            progreso.masa_muscular = float(request.POST.get('masa_muscular')) if request.POST.get('masa_muscular') else None
            progreso.agua_corporal = float(request.POST.get('agua_corporal')) if request.POST.get('agua_corporal') else None
            progreso.tension_arterial_maxima = float(request.POST.get('tension_arterial_maxima')) if request.POST.get('tension_arterial_maxima') else None
            progreso.tension_arterial_minima = float(request.POST.get('tension_arterial_minima')) if request.POST.get('tension_arterial_minima') else None
            progreso.comentario = request.POST.get('comentario', '')
            progreso.save()
            messages.success(request, 'Datos de evolución actualizados exitosamente')
            return redirect('pacientes:infopaciente', persona_id=paciente.persona_id)
        except Progreso.DoesNotExist:
            messages.error(request, 'No se encontraron datos para la fecha seleccionada')
        except ValueError as e:
            messages.error(request, f'Error en los datos numéricos: {str(e)}')
        except Exception as e:
            messages.error(request, f'Error al actualizar evolución: {str(e)}')
    
    return redirect('pacientes:infopaciente_detalle', paciente_id=paciente.pk)