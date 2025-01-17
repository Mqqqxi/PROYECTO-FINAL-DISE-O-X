"""
URL configuration for nutri project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
#URL LOGIN
from django.contrib.auth import views as auth
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home, name='inicio'),
    #LOGIN
    path('login/',auth.LoginView.as_view(template_name='pacientes/login.html'),name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path("turnos/", include("apps.turno.urls")),
    path("pacientes/",include("apps.pacientes.urls")),


    # path("comida/", include("apps.comida.urls")),
    # path("pacientes/", include("apps.pacientes.urls")),
    # path("persona/", include("apps.persona.urls")),
    # path("planNutricional/", include("apps.planNutricional.urls")),
    # path("progreso/", include("apps.progreso.urls")),
    
]

