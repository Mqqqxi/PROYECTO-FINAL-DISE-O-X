import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Turno
from apps.pacientes.models import Paciente
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
@login_required
def Turnos(request):

	return render(request, 'turnos/turnos.html')



@login_required
def reservar_turnos(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        dia = data.get('dia')  # Fecha seleccionada
        hora = data.get('hora')  # Hora seleccionada
        motivo = data.get('motivo')  # Motivo seleccionado

        if not dia or not hora or not motivo:
            return JsonResponse({'success': False, 'error': 'Faltan datos para la reserva.'}, status=400)

        # Obtén el paciente logueado
        try:
            paciente = Paciente.objects.get(persona=request.user)
        except Paciente.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Paciente no encontrado.'}, status=404)

        # Verifica si el paciente ya tiene un turno reservado
        turno_existente = Turno.objects.filter(paciente=paciente).first()
        if turno_existente:
            return JsonResponse({
                'success': False,
                'error': f'Ya tienes un turno reservado el día {turno_existente.dia} a las {turno_existente.hora.strftime("%H:%M")}.'
            }, status=400)

        # Crea el turno
        try:
            Turno.objects.create(
                paciente=paciente,
                dia=dia,
                hora=hora,
                motivo=motivo
            )
            return JsonResponse({'success': True, 'message': 'Turno reservado exitosamente.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
def obtener_horarios_ocupados(request):
    dia = request.GET.get('dia')  # Día en formato 'YYYY-MM-DD'
    if dia:
        horarios = Turno.objects.filter(dia=dia).values_list('hora', flat=True)
        return JsonResponse({'success': True, 'horarios_ocupados': list(horarios)})
    return JsonResponse({'success': False, 'error': 'Día no proporcionado.'})


@login_required
def obtener_turno(request):
    if request.method == 'GET':
        try:
            paciente = Paciente.objects.get(persona=request.user)
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
        except Paciente.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Paciente no encontrado.'}, status=404)
    return JsonResponse({'success': False, 'error': 'Método no permitido.'}, status=405)

@login_required
def cancelar_turno(request):
    if request.method == 'POST':
        try:
            paciente = Paciente.objects.get(persona=request.user)
            turno = Turno.objects.filter(paciente=paciente).first()
            if turno:
                turno.delete()
                return JsonResponse({'success': True, 'message': 'Turno cancelado exitosamente.'})
            return JsonResponse({'success': False, 'error': 'No tienes un turno reservado.'}, status=404)
        except Paciente.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Paciente no encontrado.'}, status=404)
    return JsonResponse({'success': False, 'error': 'Método no permitido.'}, status=405)
