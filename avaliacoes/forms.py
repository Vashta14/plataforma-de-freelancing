from django import forms
from .models import Avaliacao


class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['nota', 'comentario']
        widgets = {
            'comentario': forms.Textarea(attrs={
                'rows': 4,
                'class': (
                    'w-full rounded-2xl border border-purple-200 bg-white '
                    'px-4 py-3 outline-none focus:border-purple-500 '
                    'focus:ring-4 focus:ring-purple-100'
                ),
                'placeholder': 'Conte como foi sua experiência.',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nota'].widget = forms.Select(choices=[(i, i) for i in range(1, 6)])
