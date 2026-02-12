"""
Формы для анкеты гостя.
"""

from django import forms
from .models import GuestResponse


class GuestResponseForm(forms.ModelForm):
    """Форма ответа на приглашение."""

    ALCOHOL_CHOICES = [
        ('vodka', 'Водка'),
        ('kedrovka', 'Кедровка'),
        ('wine', 'Вино'),
        ('champagne', 'Шампанское'),
        ('custom', 'Свой вариант'),
        ('no_alcohol', 'Не пью алкоголь'),
    ]

    NON_ALCOHOL_CHOICES = [
        ('juice', 'Сок'),
        ('soda', 'Газировка'),
        ('water', 'Вода'),
        ('compote', 'Компот'),
        ('custom', 'Свой вариант'),
    ]

    fio = forms.CharField(
        label='Фамилия и Имя',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите фамилию и имя',
            'required': True
        })
    )
    fio_plus_one = forms.CharField(
        label='Фамилия и Имя вашего спутника/спутницы',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Если придёте с кем-то'
        })
    )
    will_attend = forms.TypedChoiceField(
        label='Сможете ли вы присутствовать',
        choices=[('true', 'Да'), ('false', 'Нет')],
        coerce=lambda x: str(x).lower() == 'true',
        empty_value=False,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )
    alcohol_preferences = forms.MultipleChoiceField(
        label='Предпочтения по алкогольным напиткам',
        choices=ALCOHOL_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )
    custom_alcohol = forms.CharField(
        label='Свой вариант алкоголя',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Укажите свой напиток'
        })
    )
    non_alcohol_preferences = forms.MultipleChoiceField(
        label='Предпочтения по безалкогольным напиткам',
        choices=NON_ALCOHOL_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )
    custom_non_alcohol = forms.CharField(
        label='Безалкогольный свой вариант',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Укажите свой напиток'
        })
    )
    overnight_stay = forms.BooleanField(
        label='Планируете ли остаться с ночевой',
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    transfer_to_venue = forms.BooleanField(
        label='Мне нужен трансфер до базы отдыха',
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    transfer_home = forms.BooleanField(
        label='Мне нужен трансфер до дома',
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    transfer_address = forms.CharField(
        label='Адрес трансфера (до дома)',
        max_length=500,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Куда нужен трансфер'
        })
    )

    class Meta:
        model = GuestResponse
        fields = [
            'fio', 'fio_plus_one', 'will_attend',
            'alcohol_preferences', 'custom_alcohol',
            'non_alcohol_preferences', 'custom_non_alcohol',
            'overnight_stay', 'transfer_to_venue', 'transfer_home',
            'transfer_address'
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.will_attend = bool(self.cleaned_data.get('will_attend'))
        if commit:
            instance.save()
        return instance
