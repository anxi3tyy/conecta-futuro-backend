from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, SolicitudServicio

class RegistroUsuarioForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('username', 'email', 'tipo_usuario',) 
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'tipo_usuario': forms.Select(attrs={'class': 'form-select'}),
        }

class SolicitudServicioForm(forms.ModelForm):
    class Meta:
        model = SolicitudServicio
        fields = ['nombre_contacto', 'email_contacto', 'telefono_contacto', 'equipo', 'descripcion_problema']
        widgets = {
            'nombre_contacto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre completo'}),
            'email_contacto': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'nombre@ejemplo.com'}),
            'telefono_contacto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+56 9 ...'}),
            'equipo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Notebook HP'}),
            'descripcion_problema': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class SolicitudInternaForm(forms.ModelForm):
    class Meta:
        model = SolicitudServicio

        fields = ['nombre_contacto', 'equipo', 'estado', 'descripcion_problema']
        
        widgets = {
            'nombre_contacto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del Dueño'}),
            'equipo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Marca y Modelo del Equipo'}),
            'estado': forms.Select(attrs={'class': 'form-select fw-bold'}),
            'descripcion_problema': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Falla reportada...'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['nombre_contacto'].label = "Dueño del Equipo"
        self.fields['descripcion_problema'].label = "Problema Reportado"
        self.fields['estado'].initial = 'pendiente'

class GestionSolicitudForm(forms.ModelForm):
    class Meta:
        model = SolicitudServicio
        fields = ['estado', 'notas_tecnicas'] 
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'notas_tecnicas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }