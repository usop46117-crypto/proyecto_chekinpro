from django.urls import path
from . import views

app_name = 'habitaciones'  # ← importante para usar namespace

urlpatterns = [
    path('', views.listar_habitaciones, name='listar'),  # lista de habitaciones
    path('crear/', views.crear_habitacion, name='crear'),
    path('editar/<int:id>/', views.editar_habitacion, name='editar'),
    path('eliminar/<int:id>/', views.eliminar_habitacion, name='eliminar'),
]
