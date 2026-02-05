from django import forms
from .models import Huesped

class HuespedForm(forms.ModelForm):
    class Meta:
        model = Huesped
        fields = '__all__'