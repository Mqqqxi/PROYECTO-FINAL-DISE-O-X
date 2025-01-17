from django.shortcuts import render, redirect
from django.contrib.auth import logout
#request 'es un diccionario que continuamente se va pasando entre el navegador y el servidor'

def Home(request):
	#print(request.user)  # Debe mostrar el usuario autenticado o AnonymousUser si no está autenticado
	return render(request, 'index.html')



def custom_logout(request):
    logout(request)
    return redirect('inicio')  # Redirige a la página de login