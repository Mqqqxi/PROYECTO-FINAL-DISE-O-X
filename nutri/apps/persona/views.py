from django.shortcuts import render, redirect
from .forms import UserRegisterForm

def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'persona/registro.html', {'form': form})