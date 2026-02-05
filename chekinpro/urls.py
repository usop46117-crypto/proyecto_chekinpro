from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('home.urls', 'home'), namespace='home')),
    path('usuarios/', include(('usuarios.urls', 'usuarios'), namespace='usuarios')),
    path('reservas/', include(('reservas.urls', 'reservas'), namespace='reservas')),
    path('habitaciones/', include(('habitaciones.urls', 'habitaciones'), namespace='habitaciones')),  # ✅ namespace
]
