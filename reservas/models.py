from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone


def fecha_hoy():
    return timezone.localdate()


def fecha_manana():
    return timezone.localdate() + timezone.timedelta(days=1)


class Reserva(models.Model):

    # ====== OPCIONES ======
    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("confirmada", "Confirmada"),
        ("cancelada", "Cancelada"),
    ]

    TIPOS_HABITACION = [
        ("individual", "Individual"),
        ("doble", "Doble"),
        ("suite", "Suite"),
        ("familiar", "Familiar"),
    ]

    TIPOS_VEHICULO = [
        ("ninguno", "Sin vehículo"),
        ("carro", "Carro"),
        ("moto", "Moto"),
        ("camioneta", "Camioneta"),
    ]

    METODOS_PAGO = [
        ("efectivo", "Efectivo"),
        ("tarjeta", "Tarjeta"),
        ("transferencia", "Transferencia"),
    ]

    # ====== USUARIO ======
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reservas"
    )

    # ====== HUÉSPED ======
    nombre = models.CharField(max_length=120)
    telefono = models.CharField(max_length=30)
    email = models.EmailField(blank=True, null=True)

    # ====== FECHAS ======
    entrada = models.DateField(default=fecha_hoy)
    salida = models.DateField(default=fecha_manana)

    # ====== HABITACIÓN ======
    tipo_habitacion = models.CharField(
        max_length=20,
        choices=TIPOS_HABITACION,
        default="individual"
    )
    habitacion = models.CharField(max_length=10)

    # ====== VEHÍCULO ======
    tipo_vehiculo = models.CharField(
        max_length=20,
        choices=TIPOS_VEHICULO,
        default="ninguno"
    )
    placa = models.CharField(max_length=10, blank=True)

    # ====== PAGO ======
    metodo_pago = models.CharField(
        max_length=20,
        choices=METODOS_PAGO,
        default="efectivo"
    )
    total = models.DecimalField(max_digits=10, decimal_places=2)

    # ====== ESTADO ======
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default="pendiente"
    )

    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creado"]

    def __str__(self):
        return f"{self.nombre} - Hab {self.habitacion}"

    # ====== VALIDACIONES ======
    def clean(self):

        if self.salida <= self.entrada:
            raise ValidationError("La fecha de salida debe ser mayor que la de entrada.")

        if self.tipo_vehiculo != "ninguno" and not self.placa:
            raise ValidationError("Debe ingresar placa si hay vehículo.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    # ====== PROPIEDADES ======
    @property
    def noches(self):
        return (self.salida - self.entrada).days

