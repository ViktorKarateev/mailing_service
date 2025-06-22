from django import forms
from .models import Mailing


class MailingForm(forms.ModelForm):
    start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label='Время начала',
        input_formats=['%Y-%m-%dT%H:%M']
    )
    end_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label='Время окончания',
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = Mailing
        fields = ['start_time', 'end_time', 'status', 'message', 'clients']
        labels = {
            'status': 'Статус',
            'message': 'Сообщение',
            'clients': 'Клиенты',
        }
