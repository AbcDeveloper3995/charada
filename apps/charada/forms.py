from django.forms import *

from apps.charada.models import Limitado, Tiro


class limitadoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Limitado
        fields = '__all__'
        widgets = {
            'numero': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un numero', 'id': 'numeroLimitado'}),
            'tipo': Select(attrs={'class': 'form-control', 'placeholder': 'Seleccione una opcion', 'id': 'tipoLimitado'}),
            'precio': NumberInput(attrs={'class': 'form-control', 'readonly':True, 'id': 'precioLimitado'}),
        }

class tiroForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Tiro
        fields = '__all__'
        widgets = {
            'primerNumero': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un numero', 'id': 'primerNumero', 'required': True}),
            'fijoCorrido': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un numero', 'id': 'fijoCorrido', 'required': True}),
            'primerCorrido': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un numero', 'id': 'primerCorrido', 'required': True}),
            'segundoCorrido': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un numero', 'id': 'segundoCorrido', 'required': True}),
            'horario': Select(attrs={'class': 'form-control', 'placeholder': 'Seleccione una opcion', 'id': 'horario', 'required': True}),
        }

    def clean_primerNumero(self):
        data = str(self.cleaned_data['primerNumero'])
        if len(data) != 1:
            raise forms.ValidationError("La centena debe ser un numero de solo 1 digito.")
        return data

    def clean_fijoCorrido(self):
        data = str(self.cleaned_data['fijoCorrido'])
        if len(data) != 2:
            raise forms.ValidationError("El fijo debe ser un numero de solo 2 digitos.")
        return data

    def clean_primerCorrido(self):
        data = str(self.cleaned_data['primerCorrido'])
        if len(data) != 2:
            raise forms.ValidationError("Los corridos deben ser un numero de solo 2 digitos.")
        return data

    def clean_segundoCorrido(self):
        data = str(self.cleaned_data['segundoCorrido'])
        if len(data) != 2:
            raise forms.ValidationError("Los corridos deben ser un numero de solo 2 digitos.")
        return data


