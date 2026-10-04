from django import forms
from apps.dashboard.models import Dataimpor


class DataimporForm(forms.ModelForm):
    class Meta:
        model = Dataimpor
        fields = ['titulo', 'descricao', 'data']

        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),

            'data': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            })
        }