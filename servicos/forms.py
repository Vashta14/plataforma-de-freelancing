from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Servico


class CriarServicoForm(forms.ModelForm):
    data_hora = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'w-full rounded-xl border border-purple-300 px-4 py-3 focus:border-purple-600 focus:outline-none focus:ring-2 focus:ring-purple-200 text-base',
            'style': 'cursor: pointer; font-size: 16px;',
        }),
        label='Data e Hora do Serviço',
        help_text='Selecione a data e hora do serviço',
    )
    
    class Meta:
        model = Servico
        fields = ('nome', 'descricao', 'data_hora', 'valor_hora', 'duracao')
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-purple-300 px-4 py-3 focus:border-purple-600 focus:outline-none focus:ring-2 focus:ring-purple-200',
                'placeholder': 'Ex: Desenvolvimento de website em React',
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'w-full rounded-xl border border-purple-300 px-4 py-3 focus:border-purple-600 focus:outline-none focus:ring-2 focus:ring-purple-200',
                'rows': 6,
                'placeholder': 'Descreva detalhadamente o que você precisa...',
            }),
            'valor_hora': forms.NumberInput(attrs={
                'class': 'w-full rounded-xl border border-purple-300 px-4 py-3 focus:border-purple-600 focus:outline-none focus:ring-2 focus:ring-purple-200',
                'placeholder': '100.00',
                'step': '0.01',
                'min': '0.01',
            }),
            'duracao': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-purple-300 px-4 py-3 focus:border-purple-600 focus:outline-none focus:ring-2 focus:ring-purple-200',
                'placeholder': 'Ex: 40 horas, 1 semana, 2 dias',
            }),
        }
        labels = {
            'nome': 'Título do Serviço',
            'descricao': 'Descrição',
            'valor_hora': 'Valor/Hora (R$)',
            'duracao': 'Duração Estimada',
        }
    
    def clean_valor_hora(self):
        valor_hora = self.cleaned_data.get('valor_hora')
        if valor_hora and valor_hora <= 0:
            raise ValidationError('O valor/hora deve ser maior que zero.')
        return valor_hora
    
    def clean_data_hora(self):
        data_hora = self.cleaned_data.get('data_hora')
        if data_hora and data_hora < timezone.now():
            raise ValidationError('A data e hora devem ser futuras.')
        return data_hora
