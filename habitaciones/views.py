from django.shortcuts import render, redirect, get_object_or_404
from .models import Habitacion
from .forms import HabitacionForm

#  Lista todas las habitaciones
def listar_habitaciones(request):
    habitaciones = Habitacion.objects.all()
    return render(request, 'habitaciones/lista.html', {'habitaciones': habitaciones})

#  Crear habitación
def crear_habitacion(request):
    if request.method == 'POST':
        form = HabitacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('habitaciones:listar')  # usa namespace
    else:
        form = HabitacionForm()
    return render(request, 'habitaciones/form.html', {'form': form})

# Editar habitación
def editar_habitacion(request, id):
    habitacion = get_object_or_404(Habitacion, id=id)
    if request.method == 'POST':
        form = HabitacionForm(request.POST, instance=habitacion)
        if form.is_valid():
            form.save()
            return redirect('habitaciones:listar')
    else:
        form = HabitacionForm(instance=habitacion)
    return render(request, 'habitaciones/form.html', {'form': form})

#  Eliminar habitación
def eliminar_habitacion(request, id):
    habitacion = get_object_or_404(Habitacion, id=id)
    habitacion.delete()
    return redirect('habitaciones:listar')
