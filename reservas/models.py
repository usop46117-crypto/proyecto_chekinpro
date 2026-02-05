from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone


def fecha_hoy():
    """Default para fecha_entrada (evita preguntas en migraciones)."""
    return timezone.localdate()


def fecha_manana():
    """Default para fecha_salida (evita preguntas en migraciones)."""
    return timezone.localdate() + timezone.timedelta(days=1)


class Reserva(models.Model):
    # -------------------------
    # Choices (TextChoices PRO)
    # -------------------------
    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        CONFIRMADA = "confirmada", "Confirmada"
        CANCELADA = "cancelada", "Cancelada"

    class TipoHabitacion(models.TextChoices):
        INDIVIDUAL = "individual", "Individual"
        DOBLE = "doble", "Doble"
        SUITE = "suite", "Suite"
        FAMILIAR = "familiar", "Familiar"

    class TipoVehiculo(models.TextChoices):
        NINGUNO = "ninguno", "Sin vehículo"
        CARRO = "carro", "Carro"
        MOTO = "moto", "Moto"
        CAMIONETA = "camioneta", "Camioneta"

    class MetodoPago(models.TextChoices):
        EFECTIVO = "efectivo", "Efectivo"
        TARJETA = "tarjeta", "Tarjeta"
        TRANSFERENCIA = "transferencia", "Transferencia"

    # -------------------------
    # Usuario del sistema
    # -------------------------
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reservas",
        verbose_name="Creada por",
    )

    # -------------------------
    # Datos del huésped (NO es usuario)
    # -------------------------
    nombre_huesped = models.CharField("Nombre del huésped", max_length=120)

    documento = models.CharField(
        "Documento",
        max_length=20,
        blank=True,
        default="",
        help_text="Cédula / pasaporte del huésped (si no tiene, se deja vacío).",
    )

    telefono = models.CharField("Teléfono", max_length=30)

    email = models.EmailField("Correo", blank=True, null=True)

    # -------------------------
    # Fechas
    # -------------------------
    fecha_entrada = models.DateField("Fecha de entrada", default=fecha_hoy)
    fecha_salida = models.DateField("Fecha de salida", default=fecha_manana)

    # -------------------------
    # Ocupación
    # -------------------------
    adultos = models.PositiveSmallIntegerField("Adultos", default=1)
    ninos = models.PositiveSmallIntegerField("Niños", default=0)

    # -------------------------
    # Habitación
    # -------------------------
    tipo_habitacion = models.CharField(
        "Tipo de habitación",
        max_length=20,
        choices=TipoHabitacion.choices,
        default=TipoHabitacion.INDIVIDUAL,
    )

    habitacion = models.CharField(
        "Habitación",
        max_length=10,
        default="POR_ASIGNAR",
        help_text="Ej: 101, 305, A12",
    )

    # -------------------------
    # Vehículo
    # -------------------------
    tipo_vehiculo = models.CharField(
        "Vehículo",
        max_length=20,
        choices=TipoVehiculo.choices,
        default=TipoVehiculo.NINGUNO,
    )

    placa = models.CharField("Placa", max_length=10, blank=True, default="")
    color_vehiculo = models.CharField("Color vehículo", max_length=30, blank=True, default="")

    # -------------------------
    # Pago
    # -------------------------
    metodo_pago = models.CharField(
        "Método de pago",
        max_length=20,
        choices=MetodoPago.choices,
        default=MetodoPago.EFECTIVO,
    )

    total = models.DecimalField("Total", max_digits=12, decimal_places=2, default=0)

    # -------------------------
    # Extra
    # -------------------------
    observaciones = models.TextField("Observaciones", blank=True, default="")

    estado = models.CharField(
        "Estado",
        max_length=20,
        choices=Estado.choices,
        default=Estado.PENDIENTE,
    )

    creado = models.DateTimeField("Creado", auto_now_add=True)

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ["-creado"]

    def __str__(self):
        return f"Reserva #{self.id} - {self.nombre_huesped}"

    # -------------------------
    # Validaciones reales
    # -------------------------
    def clean(self):
        errors = {}

        # Fecha salida debe ser mayor que entrada
        if self.fecha_salida and self.fecha_entrada:
            if self.fecha_salida <= self.fecha_entrada:
                errors["fecha_salida"] = "La fecha de salida debe ser posterior a la fecha de entrada."

        # Adultos mínimo 1
        if self.adultos is not None and self.adultos < 1:
            errors["adultos"] = "Debe haber mínimo 1 adulto."

        # Si hay vehículo, placa obligatoria
        if self.tipo_vehiculo != self.TipoVehiculo.NINGUNO:
            if not (self.placa or "").strip():
                errors["placa"] = "La placa es obligatoria si el huésped trae vehículo."
        else:
            # Si no hay vehículo, limpia placa y color
            self.placa = ""
            self.color_vehiculo = ""

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        # Garantiza validaciones al guardar desde admin / forms
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def total_personas(self):
        return int(self.adultos or 0) + int(self.ninos or 0)

    @property
    def noches(self):
        if self.fecha_salida and self.fecha_entrada:
            return max((self.fecha_salida - self.fecha_entrada).days, 0)
        return 0
