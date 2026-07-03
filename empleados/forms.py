from django import forms
from .models import Cargo, Empleado

FIELD_CLASS = {'class': 'form-control'}
SELECT_CLASS = {'class': 'form-select'}

class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = '__all__'
        widgets = {
            'nombre':      forms.TextInput(attrs={**FIELD_CLASS, 'placeholder': 'Ej: Gerente General'}),
            'descripcion': forms.TextInput(attrs={**FIELD_CLASS, 'placeholder': 'Descripción breve (opcional)'}),
        }

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = '__all__'
        widgets = {
            'nombres':       forms.TextInput(attrs={**FIELD_CLASS, 'placeholder': 'Nombres'}),
            'apellidos':     forms.TextInput(attrs={**FIELD_CLASS, 'placeholder': 'Apellidos'}),
            'correo':        forms.EmailInput(attrs={**FIELD_CLASS, 'placeholder': 'correo@ejemplo.com'}),
            'sueldo':        forms.NumberInput(attrs={**FIELD_CLASS, 'placeholder': '0.00'}),
            'fecha_ingreso': forms.DateInput(attrs={**FIELD_CLASS, 'type': 'date'}),
            'cargo':         forms.Select(attrs=SELECT_CLASS),
        }
