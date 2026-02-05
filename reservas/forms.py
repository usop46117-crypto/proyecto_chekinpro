from django import forms
from .models import Reserva
from datetime import date


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        exclude = ("usuario", "creado", "total")

        widgets = {
            "fecha_entrada": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "fecha_salida": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "observaciones": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # estilos bootstrap para todos los campos
        for name, field in self.fields.items():
            if not isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({"class": "form-control"})

    def clean(self):
        cleaned = super().clean()

        entrada = cleaned.get("fecha_entrada")
        salida = cleaned.get("fecha_salida")
        tipo_vehiculo = cleaned.get("tipo_vehiculo")
        placa = cleaned.get("placa")

        if entrada and salida:
            if salida <= entrada:
                raise forms.ValidationError("La fecha de salida debe ser mayor a la fecha de entrada.")
            if entrada < date.today():
                raise forms.ValidationError("La fecha de entrada no puede ser menor a hoy.")

        # si hay vehículo, placa obligatoria
        if tipo_vehiculo and tipo_vehiculo != "ninguno":
            if not placa:
                raise forms.ValidationError("Si seleccionas vehículo, la placa es obligatoria.")

        return cleaned
