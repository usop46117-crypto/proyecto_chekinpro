from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario


class UsuarioRegistroForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Correo electrónico'
        })
    )

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Nombre de usuario'
            }),
        }
