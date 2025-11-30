from django import forms
from .models import Curso

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nombre_curso', 'descripcion', 'duracion', 'modalidad']
        widgets = {
            'nombre_curso': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Introducción a Python'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe de qué trata el curso...'}),
            'duracion': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Horas totales'}),
            'modalidad': forms.Select(choices=[('Presencial', 'Presencial'), ('Online', 'Online'), ('Híbrido', 'Híbrido')], attrs={'class': 'form-select'}),
        }