from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistroPacienteForm

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
            if user.is_paciente:  # Verificar que sea un paciente
                login(request, user)
                return redirect('inicio')  # Redirige a la página principal o donde prefieras
            else:
                form.add_error(None, 'Solo los pacientes pueden iniciar sesión.')
    else:
        form = AuthenticationForm()
    return render(request, 'pacientes/login.html', {'form': form})
