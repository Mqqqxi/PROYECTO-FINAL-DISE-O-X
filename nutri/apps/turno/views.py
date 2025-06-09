from datetime import datetime
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.utils.dateparse import parse_date

from apps.persona.models import Nutricionista
from .models import Turno
from apps.pacientes.models import Paciente

@login_required
def Turnos(request):
    # Usar el campo is_nutricionista del modelo Persona directamente
    is_nutricionista = request.user.is_nutricionista
    return render(request, 'turnos/turnos.html', {
        'is_nutricionista': is_nutricionista
    })


from django.db import transaction
from django.db.models import Q

@login_required
def reservar_turnos(request):
    if request.user.is_nutricionista:
        return JsonResponse({'success': False, 'error': 'No tienes permisos para reservar turnos.'}, status=403)
    
    if not request.user.is_paciente:
        return JsonResponse({'success': False, 'error': 'No estás registrado como paciente.'}, status=403)
    
    try:
        paciente = Paciente.objects.get(persona=request.user)
    except Paciente.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'No estás registrado como paciente.'}, status=403)
    
    if request.method == 'POST':
        data = json.loads(request.body)
        dia = data.get('dia')  # Fecha seleccionada (YYYY-MM-DD)
        hora = data.get('hora')  # Hora seleccionada (HH:MM)
        motivo = data.get('motivo')  # Motivo seleccionado

        if not dia or not hora or not motivo:
            return JsonResponse({'success': False, 'error': 'Faltan datos para la reserva.'}, status=400)

        # Validar fecha
        try:
            parsed_date = datetime.strptime(dia, '%Y-%m-%d').date()
            day_of_week = parsed_date.weekday()  # 0 = Lunes, 6 = Domingo
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Formato de fecha inválido.'}, status=400)

        # Validar que no sea domingo
        if day_of_week == 6:  # Domingo
            return JsonResponse({'success': False, 'error': 'No se pueden reservar turnos los domingos.'}, status=400)

        # Validar horarios en sábados
        if day_of_week == 5:  # Sábado
            try:
                parsed_time = datetime.strptime(hora, '%H:%M').time()
                hour, minute = parsed_time.hour, parsed_time.minute
                time_in_minutes = hour * 60 + minute
                if 16 * 60 <= time_in_minutes <= 19 * 60 + 30:  # 16:00 a 19:30
                    return JsonResponse({'success': False, 'error': 'No se pueden reservar turnos los sábados entre las 16:00 y las 19:30.'}, status=400)
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Formato de hora inválido.'}, status=400)

        # Verifica si el paciente ya tiene un turno reservado
        turno_existente = Turno.objects.filter(paciente=paciente).first()
        if turno_existente:
            return JsonResponse({
                'success': False,
                'error': f'Ya tienes un turno reservado el día {turno_existente.dia} a las {turno_existente.hora.strftime("%H:%M")}.'
            }, status=400)

        # Verifica si ya existe un turno en el mismo día y hora
        with transaction.atomic():
            turno_ocupado = Turno.objects.filter(dia=dia, hora=hora).exists()
            if turno_ocupado:
                return JsonResponse({
                    'success': False,
                    'error': f'El horario {hora} del día {dia} ya está ocupado.'
                }, status=400)

            # Obtener la única nutricionista
            try:
                nutricionista = Nutricionista.objects.get()
            except Nutricionista.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'No hay una nutricionista registrada.'}, status=500)

            # Crea el turno
            try:
                Turno.objects.create(
                    paciente=paciente,
                    nutricionista=nutricionista,
                    dia=dia,
                    hora=hora,
                    motivo=motivo
                )
                return JsonResponse({'success': True, 'message': 'Turno reservado exitosamente.'})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Método no permitido.'}, status=405)

@login_required
def obtener_horarios_ocupados(request):
    dia = request.GET.get('dia')  # Día en formato 'YYYY-MM-DD'
    if dia:
        horarios = Turno.objects.filter(dia=dia).values_list('hora', flat=True)
        return JsonResponse({'success': True, 'horarios_ocupados': list(horarios)})
    return JsonResponse({'success': False, 'error': 'Día no proporcionado.'}, status=400)

@login_required
def obtener_turno(request):
    if request.user.is_nutricionista:
        return JsonResponse({'success': True, 'turno': None})

    if not request.user.is_paciente:
        return JsonResponse({'success': True, 'turno': None})

    try:
        paciente = Paciente.objects.get(persona=request.user)
    except Paciente.DoesNotExist:
        return JsonResponse({'success': True, 'turno': None})

    if request.method == 'GET':
        turno = Turno.objects.filter(paciente=paciente).first()
        if turno:
            return JsonResponse({
                'success': True,
                'turno': {
                    'id': turno.idTurno,
                    'dia': turno.dia,
                    'hora': turno.hora.strftime('%H:%M'),
                    'motivo': turno.motivo,
                }
            })
        return JsonResponse({'success': True, 'turno': None})
    return JsonResponse({'success': False, 'error': 'Método no permitido.'}, status=405)

@login_required
def cancelar_turno(request):
    if request.user.is_nutricionista:
        return JsonResponse({'success': False, 'error': 'No tienes permisos para cancelar turnos.'}, status=403)
    
    if not request.user.is_paciente:
        return JsonResponse({'success': False, 'error': 'No estás registrado como paciente.'}, status=403)
    
    try:
        paciente = Paciente.objects.get(persona=request.user)
    except Paciente.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'No estás registrado como paciente.'}, status=403)
    
    if request.method == 'POST':
        turno = Turno.objects.filter(paciente=paciente).first()
        if turno:
            turno.delete()
            return JsonResponse({'success': True, 'message': 'Turno cancelado exitosamente.'})
        return JsonResponse({'success': False, 'error': 'No tienes un turno reservado.'}, status=404)
    return JsonResponse({'success': False, 'error': 'Método no permitido.'}, status=405)

@login_required
def obtener_turnos_dia(request):
    # Verificar si el usuario es nutricionista
    if not request.user.is_nutricionista:
        raise PermissionDenied("Solo los nutricionistas pueden acceder a esta información.")

    dia = request.GET.get('dia')  # Día en formato 'YYYY-MM-DD'
    if not dia:
        return JsonResponse({'success': False, 'error': 'Día no proporcionado.'}, status=400)

    try:
        parsed_date = parse_date(dia)
        if not parsed_date:
            return JsonResponse({'success': False, 'error': 'Formato de fecha inválido.'}, status=400)

        turnos = Turno.objects.filter(dia=dia).select_related('paciente__persona')
        turnos_data = [
            {
                'id_turno': turno.idTurno,  # Añadido para identificar el turno
                'paciente_nombre': turno.paciente.persona.first_name + ' ' + turno.paciente.persona.last_name,
                'paciente_telefono': turno.paciente.persona.telefono or '',
                'hora': turno.hora.strftime('%H:%M'),
                'motivo': turno.motivo,
            }
            for turno in turnos
        ]
        return JsonResponse({'success': True, 'turnos': turnos_data})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
def eliminar_turno(request):
    if not request.user.is_nutricionista:
        return JsonResponse({'success': False, 'error': 'No tienes permisos para eliminar turnos.'}, status=403)

    if request.method == 'DELETE':
        id_turno = request.GET.get('id_turno')
        if not id_turno:
            return JsonResponse({'success': False, 'error': 'ID del turno no proporcionado.'}, status=400)

        try:
            turno = Turno.objects.get(idTurno=id_turno)
            turno.delete()
            return JsonResponse({'success': True, 'message': 'Turno eliminado exitosamente.'})
        except Turno.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'El turno no existe.'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Método no permitido.'}, status=405)