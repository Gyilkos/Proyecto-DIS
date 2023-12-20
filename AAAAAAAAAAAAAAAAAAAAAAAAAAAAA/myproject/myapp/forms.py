# myapp/forms.py
from django import forms
from .models import Camioneta

class CamionetaForm(forms.ModelForm):
    class Meta:
        model = Camioneta
        fields = ['patente']
        