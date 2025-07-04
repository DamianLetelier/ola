from django import forms
from crud_Matias.models import Empleado

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['nombre', 'apellido', 'email', 'edad', 'genero', 'salario', 'imagen']
