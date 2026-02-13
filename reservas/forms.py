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

        # Bootstrap a todos los campos sin duplicar clases
        for field in self.fields.values():
            existing_classes = field.widget.attrs.get("class", "")
            if "form-control" not in existing_classes:
                field.widget.attrs["class"] = existing_classes + " form-control"

    def clean(self):
        cleaned = super().clean()

        entrada = cleaned.get("fecha_entrada")
        salida = cleaned.get("fecha_salida")
        tipo_vehiculo = cleaned.get("tipo_vehiculo")
        placa = cleaned.get("placa")

        # Validación fechas
        if entrada and salida:
            if salida <= entrada:
                self.add_error(
                    "fecha_salida",
                    "La fecha de salida debe ser mayor a la fecha de entrada."
                )

            if entrada < date.today():
                self.add_error(
                    "fecha_entrada",
                    "La fecha de entrada no puede ser menor a hoy."
                )

        # Validación vehículo
        if tipo_vehiculo and tipo_vehiculo != "ninguno":
            if not placa:
                self.add_error(
                    "placa",
                    "Si seleccionas vehículo, la placa es obligatoria."
                )

        return cleaned

