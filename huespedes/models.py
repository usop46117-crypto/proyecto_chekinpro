from django.db import models

class Huesped(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"