from django import forms
from .models import Reserva
from datetime import date


class ReservaForm(forms.ModelForm):

    fecha_entrada = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control"
            }
        )
    )

    fecha_salida = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = Reserva
        exclude = ("usuario", "creado", "total")

        widgets = {
            "observaciones": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "form-control"
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Aplicar Bootstrap a todos los campos
        for field in self.fields.values():
            if "class" not in field.widget.attrs:
                field.widget.attrs["class"] = "form-control"

    def clean(self):
        cleaned = super().clean()

        entrada = cleaned.get("fecha_entrada")
        salida = cleaned.get("fecha_salida")
        tipo_vehiculo = cleaned.get("tipo_vehiculo")
        placa = cleaned.get("placa")

        # Validación fechas
        if entrada and salida:
            if salida <= entrada:
                raise forms.ValidationError(
                    "La fecha de salida debe ser mayor a la fecha de entrada."
                )

            if entrada < date.today():
                raise forms.ValidationError(
                    "La fecha de entrada no puede ser menor a hoy."
                )

        # Validación vehículo
        if tipo_vehiculo and tipo_vehiculo != "ninguno":
            if not placa:
                raise forms.ValidationError(
                    "Si seleccionas vehículo, la placa es obligatoria."
                )

        return cleaned


