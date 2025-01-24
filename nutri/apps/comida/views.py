from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ComidaForm
from .models import Comida


# Create your views here.
def comida(request):
    comidas = Comida.objects.all()  # Obtén todas las comidas de la base de datos
    return render(request, 'comida/comida.html', {'comidas': comidas})


def agregar_comida(request):
    if request.method == 'POST':
        form = ComidaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('comida:comida')  # Redirige a la página de comida o donde desees
    else:
        form = ComidaForm()
    return render(request, 'comida/agregar_comida.html', {'form': form})


def plato(request):
    return render(request, 'comida/platocomida.html')