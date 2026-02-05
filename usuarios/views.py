from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView

from .models import PerfilUsuario


class UsuarioLoginView(LoginView):
    template_name = 'usuarios/login.html'

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)

        # ✅ Redirección por rol
        try:
            perfil = PerfilUsuario.objects.get(user=user)

            if perfil.rol == 'ADMIN':
                return redirect('home:index')  # o dashboard admin
            else:
                return redirect('reservas:listar')  # ✅ CORREGIDO

        except PerfilUsuario.DoesNotExist:
            return redirect('home:index')


def register_view(request):
    """
    Registro solo para ADMIN / RECEPCIONISTA
    """
    if request.method == "POST":
        username = request.POST.get("username")
        rol = request.POST.get("rol")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Validaciones
        if not username or not password1 or not password2 or not rol:
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect("usuarios:registrar")

        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect("usuarios:registrar")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Ese usuario ya existe.")
            return redirect("usuarios:registrar")

        # Crear usuario
        user = User.objects.create_user(username=username, password=password1)

        # Crear perfil con rol
        PerfilUsuario.objects.create(user=user, rol=rol)

        messages.success(request, f"Usuario '{username}' registrado correctamente. Ya puedes iniciar sesión.")
        return redirect("usuarios:login")

    return render(request, "usuarios/registrar.html")
