from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import timedelta

from .models import Reserva
from .forms import ReservaForm


def calcular_total(reserva: Reserva):
    """
    Total real (ejemplo):
    - precio por noche según tipo habitación
    - + adicional por adulto extra
    - + adicional por niño
    - + parqueadero si hay vehículo
    """

    precios = {
        "individual": 90000,
        "doble": 140000,
        "suite": 250000,
        "familiar": 200000,
    }

    base = precios.get(reserva.tipo_habitacion, 100000)

    noches = (reserva.fecha_salida - reserva.fecha_entrada).days
    if noches <= 0:
        noches = 1

    total = base * noches

    # extras
    if reserva.adultos > 1:
        total += (reserva.adultos - 1) * 20000 * noches

    if reserva.ninos > 0:
        total += reserva.ninos * 10000 * noches

    # parqueadero
    if reserva.tipo_vehiculo != "ninguno":
        total += 15000 * noches

    return total


@login_required
def listar(request):
    reservas = Reserva.objects.all().order_by("-creado")
    return render(request, "reservas/listar.html", {"reservas": reservas})


@login_required
def crear(request):
    if request.method == "POST":
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.usuario = request.user

            reserva.total = calcular_total(reserva)
            reserva.save()

            messages.success(request, "Reserva creada correctamente ✅")
            return redirect("reservas:listar")
        else:
            messages.error(request, "Corrige los errores del formulario.")
    else:
        form = ReservaForm()

    return render(request, "reservas/crear.html", {"form": form})


@login_required
def editar(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)

    if request.method == "POST":
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.total = calcular_total(reserva)
            reserva.save()

            messages.success(request, "Reserva actualizada correctamente ✅")
            return redirect("reservas:listar")
        else:
            messages.error(request, "Corrige los errores del formulario.")
    else:
        form = ReservaForm(instance=reserva)

    return render(request, "reservas/editar.html", {"form": form, "reserva": reserva})


@login_required
def eliminar(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)

    if request.method == "POST":
        reserva.delete()
        messages.success(request, "Reserva eliminada correctamente 🗑️")
        return redirect("reservas:listar")

    return render(request, "reservas/eliminar.html", {"reserva": reserva})
