from django import forms
from .models import PlanoAlimentar

class PlanoAlimentarForm(forms.ModelForm):
    class Meta:
        model = PlanoAlimentar
        fields = ['dia_semana', 'tipo_refeicao', 'descricao', 'calorias', 'concluido']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Ex: Pão, ovo cozido, café...'}),
        }
