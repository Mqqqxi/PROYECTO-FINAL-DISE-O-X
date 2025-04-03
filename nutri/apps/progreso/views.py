from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Progreso, FotoProgreso
from apps.pacientes.models import Paciente
from apps.persona.models import Nutricionista
from django.utils import timezone
from django.http import JsonResponse

def CrearProgreso(request, paciente_pk):
    paciente = get_object_or_404(Paciente, pk=paciente_pk)
    progresos = Progreso.objects.filter(paciente=paciente).order_by('-fecha')

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        # Formulario de evolución
        if form_type == 'evolucion':
            try:
                progreso = Progreso(
                    paciente=paciente,
                    fecha=request.POST.get('fecha'),
                    peso=float(request.POST.get('peso')) if request.POST.get('peso') else 0.0,  # Peso obligatorio
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
                return redirect('progreso:crear_progreso', paciente_pk=paciente.pk)
            except ValueError as e:
                messages.error(request, f'Error en los datos numéricos: {str(e)}')
            except Exception as e:
                messages.error(request, f'Error al guardar evolución: {str(e)}')

        # Formulario de fotos
        elif form_type == 'fotos':
            try:
                progreso, created = Progreso.objects.get_or_create(
                    paciente=paciente,
                    fecha=request.POST.get('fecha', timezone.now().date()),
                    defaults={'peso': 0.0}  # Peso obligatorio por el modelo
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
                return redirect('progreso:crear_progreso', paciente_pk=paciente.pk)
            except Exception as e:
                messages.error(request, f'Error al guardar fotos: {str(e)}')

    fechas = progresos.values_list('fecha', flat=True).distinct()

    context = {
        'paciente': paciente,
        'fechas': fechas,
        'progresos': progresos,
    }
    return render(request, 'progreso/progreso.html', context)

# Vista AJAX para obtener datos y fotos de una fecha específica
def obtener_datos_progreso(request, paciente_pk, fecha):
    paciente = get_object_or_404(Paciente, pk=paciente_pk)
    progreso = get_object_or_404(Progreso, paciente=paciente, fecha=fecha)
    fotos = progreso.fotos.all()  # Obtener las fotos asociadas

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