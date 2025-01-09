from django.urls import path
from . import views 

urlpatterns = {
    path("comida", views.index , name = "index"),
}