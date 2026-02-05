from django.db import models

class Habitacion(models.Model):
    nombre = models.CharField(max_length=100, default="Habitación por defecto")
    descripcion = models.TextField(default="Sin descripción")
    precio = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    capacidad = models.IntegerField(default=1)

    def __str__(self):
        return self.nombre
