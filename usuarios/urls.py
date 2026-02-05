from django.urls import path
from .views import UsuarioLoginView, register_view
from django.contrib.auth.views import LogoutView

app_name = 'usuarios'

urlpatterns = [
    path('login/', UsuarioLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='usuarios:login'), name='logout'),
    path('registrar/', register_view, name='registrar'),
]
