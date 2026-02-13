from django import forms
from .models import Reserva
from datetime import date


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        exclude = ("usuario", "creado", "total")

        widgets = {
            "fecha_entrada": forms.DateInput(attrs={"type": "date"}),
            "fecha_salida": forms.DateInput(attrs={"type": "date"}),
            "observaciones": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

forms-reservas1
        # Bootstrap a TODOS los campos correctamente
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

        # Bootstrap para todos los campos
        for field in self.fields.values():
            existing_classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = existing_classes + " form-control"
 master

    def clean(self):
        cleaned = super().clean()

        entrada = cleaned.get("fecha_entrada")
        salida = cleaned.get("fecha_salida")
        tipo_vehiculo = cleaned.get("tipo_vehiculo")
        placa = cleaned.get("placa")

        if entrada and salida:
            if salida <= entrada:
 forms-reservas1
                raise forms.ValidationError(
                    "La fecha de salida debe ser mayor a la fecha de entrada."
                )
            if entrada < date.today():
                raise forms.ValidationError(
                    "La fecha de entrada no puede ser menor a hoy."
                )

        if tipo_vehiculo and tipo_vehiculo != "ninguno":
            if not placa:
                raise forms.ValidationError(
                    "Si seleccionas vehículo, la placa es obligatoria."
                )
                self.add_error("fecha_salida", "La fecha de salida debe ser mayor a la fecha de entrada.")

        if entrada and entrada < date.today():
            self.add_error("fecha_entrada", "La fecha de entrada no puede ser menor a hoy.")

        if tipo_vehiculo and not placa:
            self.add_error("placa", "Si seleccionas vehículo, la placa es obligatoria.")
            master

        return cleaned

