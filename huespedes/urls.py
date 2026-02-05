from django.urls import path
from .views import (
    lista_huespedes,
    crear_huesped,
    editar_huesped,
    eliminar_huesped
)

urlpatterns = [
    path('', lista_huespedes, name='lista_huespedes'),
    path('crear/', crear_huesped, name='crear_huesped'),
    path('editar/<int:id>/', editar_huesped, name='editar_huesped'),
    path('eliminar/<int:id>/', eliminar_huesped, name='eliminar_huesped'),
]

