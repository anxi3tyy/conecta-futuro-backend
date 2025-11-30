from django import forms
from .models import Donacion

class DonacionForm(forms.ModelForm):
    class Meta:
        model = Donacion
        fields = ['tipo', 'cantidad', 'descripcion']
        
        widgets = {
            'tipo': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ej. Dinero, Insumos, Equipos Tecnológicos...'
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': 1,
                'placeholder': 'Cantidad'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Detalla el estado o características de la donación.'
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo'].label = "Tipo de Donación"
        self.fields['cantidad'].label = "Cantidad / Monto"
        self.fields['descripcion'].label = "Descripción"