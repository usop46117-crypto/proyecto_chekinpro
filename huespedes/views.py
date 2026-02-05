from django.shortcuts import render, redirect
from .models import Huesped
from .forms import HuespedForm
from django.contrib import messages

def lista_huespedes(request):
    huespedes = Huesped.objects.all()
    return render(request, 'huespedes/lista.html', {'huespedes': huespedes})

def crear_huesped(request):
    if request.method == 'POST':
        form = HuespedForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_huespedes')
    else:
        form = HuespedForm()

    return render(request, 'huespedes/crear.html', {'form': form})

from django.shortcuts import get_object_or_404

def editar_huesped(request, id):
    huesped = get_object_or_404(Huesped, id=id)

    if request.method == 'POST':
        form = HuespedForm(request.POST, instance=huesped)
        if form.is_valid():
            form.save()

            messages.success(
                request,
                ' Huésped actualizado correctamente'
            )

            return redirect('lista_huespedes')
    else:
        form = HuespedForm(instance=huesped)

    return render(request, 'huespedes/editar.html', {
        'form': form
    })
    huesped = get_object_or_404(Huesped, id=id)

    if request.method == 'POST':
        form = HuespedForm(request.POST, instance=huesped)
        if form.is_valid():
            form.save()
            return redirect('lista_huespedes')
    else:
        form = HuespedForm(instance=huesped)

    return render(request, 'huespedes/editar.html', {
        'form': form
    })



def eliminar_huesped(request, id):
    huesped = get_object_or_404(Huesped, id=id)

    if request.method == 'POST':
        huesped.delete()

        messages.success(
            request,
            '🗑 Huésped eliminado correctamente'
        )

        return redirect('lista_huespedes')

    return render(request, 'huespedes/eliminar.html', {
        'huesped': huesped
    })


def crear_huesped(request):
    if request.method == 'POST':
        form = HuespedForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(
                request,
                '🎉 Huésped guardado correctamente'
            )

            return redirect('lista_huespedes')
    else:
        form = HuespedForm()

    return render(request, 'huespedes/crear.html', {
        'form': form
    })


