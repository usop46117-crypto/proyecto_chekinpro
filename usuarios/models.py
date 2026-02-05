from django.db import models
from django.contrib.auth.models import User


class PerfilUsuario(models.Model):

    class Rol(models.TextChoices):
        ADMIN = "ADMIN", "Administrador"
        RECEP = "RECEP", "Recepcionista"

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="perfil"
    )

    rol = models.CharField(
        max_length=10,
        choices=Rol.choices,
        default=Rol.RECEP
    )

    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_rol_display()}"
