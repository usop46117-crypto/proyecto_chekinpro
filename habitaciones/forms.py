from django import forms
from .models import Habitacion

class HabitacionForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields = ['nombre', 'descripcion', 'precio', 'capacidad']  # reemplaza por tus campos reales
