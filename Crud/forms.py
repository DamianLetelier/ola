from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Empresas, ForoCiberseguridad, RespuestaForo

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class EmpresasForm(forms.ModelForm):
    class Meta:
        model = Empresas
        fields = ['Nombre_Empresa', 'Cant_Empleados', 'representante', 'imagen']
        widgets = {
            'Nombre_Empresa': forms.TextInput(attrs={'class': 'form-control'}),
            'Cant_Empleados': forms.NumberInput(attrs={'class': 'form-control'}),
            'representante': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
        }

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresas
        fields = ['Nombre_Empresa', 'Cant_Empleados', 'representante', 'imagen', 'nivel_seguridad']
        widgets = {
            'Nombre_Empresa': forms.TextInput(attrs={'class': 'form-control'}),
            'Cant_Empleados': forms.NumberInput(attrs={'class': 'form-control'}),
            'representante': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
            'nivel_seguridad': forms.Select(attrs={'class': 'form-control'}),
        }

class ForoCiberseguridadForm(forms.ModelForm):
    """Formulario para crear reportes en el foro de ciberseguridad"""
    
    class Meta:
        model = ForoCiberseguridad
        fields = ['titulo', 'descripcion', 'categoria']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Describe brevemente el problema de ciberseguridad'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Describe en detalle el incidente de ciberseguridad que has experimentado. Incluye síntomas, fechas, archivos afectados, etc.'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-control'
            })
        }
        labels = {
            'titulo': 'Título del Problema',
            'descripcion': 'Descripción Detallada',
            'categoria': 'Categoría del Incidente'
        }

class RespuestaForoForm(forms.ModelForm):
    """Formulario para responder en el foro"""
    
    class Meta:
        model = RespuestaForo
        fields = ['contenido', 'es_solucion']
        widgets = {
            'contenido': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Escribe tu respuesta o solución al problema...'
            }),
            'es_solucion': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'contenido': 'Respuesta',
            'es_solucion': 'Marcar como solución'
        }

class AnalisisTextoForm(forms.Form):
    """Formulario para análisis de texto con Stanza"""
    
    texto = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 8,
            'placeholder': 'Pega aquí el texto que quieres analizar para detectar tipos de ataques cibernéticos...'
        }),
        label='Texto a Analizar',
        help_text='Describe el incidente de ciberseguridad que quieres analizar'
    )
    
    incluir_analisis_linguistico = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Incluir análisis lingüístico detallado',
        help_text='Incluye análisis de entidades nombradas y estructura gramatical'
    ) 