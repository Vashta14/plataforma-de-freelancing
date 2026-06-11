from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .models import Perfil


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'placeholder': 'seu@email.com',
        'class': 'w-full rounded-xl border border-purple-300 px-4 py-3 focus:border-purple-600 focus:outline-none focus:ring-2 focus:ring-purple-200',
    }))
    first_name = forms.CharField(label='Nome', required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Seu nome',
        'class': 'w-full rounded-xl border border-purple-300 px-4 py-3 focus:border-purple-600 focus:outline-none focus:ring-2 focus:ring-purple-200',
    }))
    last_name = forms.CharField(label='Sobrenome', required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Seu sobrenome',
        'class': 'w-full rounded-xl border border-purple-300 px-4 py-3 focus:border-purple-600 focus:outline-none focus:ring-2 focus:ring-purple-200',
    }))
    username = forms.CharField(label='Usuário', widget=forms.TextInput(attrs={
        'placeholder': 'nome de usuário',
        'class': 'w-full rounded-xl border border-purple-300 px-4 py-3 focus:border-purple-600 focus:outline-none focus:ring-2 focus:ring-purple-200',
    }))
    tipo = forms.ChoiceField(label='Tipo de conta', choices=Perfil.TIPOS_PERFIL, widget=forms.Select(attrs={
        'class': 'w-full rounded-xl border border-purple-300 px-4 py-3 focus:border-purple-600 focus:outline-none focus:ring-2 focus:ring-purple-200',
    }))
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={
        'placeholder': 'Senha',
        'class': 'w-full rounded-xl border border-purple-300 px-4 py-3 focus:border-purple-600 focus:outline-none focus:ring-2 focus:ring-purple-200',
    }))
    password2 = forms.CharField(label='Confirmar senha', widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirme a senha',
        'class': 'w-full rounded-xl border border-purple-300 px-4 py-3 focus:border-purple-600 focus:outline-none focus:ring-2 focus:ring-purple-200',
    }))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'tipo', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Perfil.objects.create(user=user, tipo=self.cleaned_data['tipo'])
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'seu@email.com',
        'class': 'w-full rounded-2xl border border-purple-300 bg-purple-50 px-4 py-3 text-purple-900 focus:border-purple-600 focus:outline-none focus:ring-2 focus:ring-purple-200',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Senha',
        'class': 'w-full rounded-2xl border border-purple-300 bg-purple-50 px-4 py-3 text-purple-900 focus:border-purple-600 focus:outline-none focus:ring-2 focus:ring-purple-200',
    }))

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
                user = authenticate(username=user.username, password=password)
                if user is None:
                    raise forms.ValidationError('Email ou senha inválidos.')
                self.user = user
            except User.DoesNotExist:
                raise forms.ValidationError('Email ou senha inválidos.')
        return self.cleaned_data

    def get_user(self):
        return self.user


FIELD_CLASS = (
    'w-full rounded-2xl border border-purple-200 bg-white px-4 py-3 '
    'text-slate-900 outline-none transition focus:border-purple-500 '
    'focus:ring-4 focus:ring-purple-100'
)


class ContaForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': FIELD_CLASS}),
            'last_name': forms.TextInput(attrs={'class': FIELD_CLASS}),
            'email': forms.EmailInput(attrs={'class': FIELD_CLASS}),
        }
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.exclude(pk=self.instance.pk).filter(email__iexact=email).exists():
            raise forms.ValidationError('Este e-mail já está em uso.')
        return email


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['descricao', 'telefone', 'endereco']
        widgets = {
            'descricao': forms.Textarea(attrs={
                'class': FIELD_CLASS,
                'rows': 5,
                'placeholder': 'Conte sobre sua experiência, especialidades e objetivos.',
            }),
            'telefone': forms.TextInput(attrs={'class': FIELD_CLASS}),
            'endereco': forms.TextInput(attrs={'class': FIELD_CLASS}),
        }
        labels = {
            'descricao': 'Descrição / Biografia',
            'telefone': 'Telefone',
            'endereco': 'Endereço',
        }

