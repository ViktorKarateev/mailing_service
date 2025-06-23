from django import forms
from django.contrib.auth.forms import UserCreationForm
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .models import CustomUser


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email', required=True)
    first_name = forms.CharField(label='Имя', required=True)
    last_name = forms.CharField(label='Фамилия', required=True)
    phone = forms.CharField(label='Телефон', required=True)
    avatar = forms.ImageField(label='Аватар', required=False)
    country = CountryField().formfield(label='Страна', widget=CountrySelectWidget)

    class Meta:
        model = CustomUser
        fields = (
            'email', 'first_name', 'last_name',
            'phone', 'avatar', 'country',
            'password1', 'password2'
        )

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email
