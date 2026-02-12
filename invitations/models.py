"""
Модель гостя для сбора информации через приглашение.
"""

from django.db import models


class GuestResponse(models.Model):
    """Ответ гостя на приглашение."""

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

    fio = models.CharField('Фамилия и Имя', max_length=255)
    fio_plus_one = models.CharField('Фамилия и Имя спутника/спутницы', max_length=255, blank=True)
    will_attend = models.BooleanField('Сможете ли вы присутствовать', default=True)

    alcohol_preferences = models.JSONField(
        'Предпочтения по алкогольным напиткам',
        default=list,
        blank=True,
        help_text='Список выбранных вариантов: vodka, kedrovka, wine, champagne, custom, no_alcohol'
    )
    custom_alcohol = models.CharField(
        'Свой вариант алкоголя',
        max_length=255,
        blank=True
    )

    non_alcohol_preferences = models.JSONField(
        'Предпочтения по безалкогольным напиткам',
        default=list,
        blank=True,
        help_text='Список выбранных: juice, soda, water, compote, custom'
    )
    custom_non_alcohol = models.CharField(
        'Безалкогольный свой вариант',
        max_length=255,
        blank=True
    )

    overnight_stay = models.BooleanField(
        'Планируете ли остаться с ночевой',
        default=False
    )
    transfer_to_venue = models.BooleanField(
        'Мне нужен трансфер до базы отдыха',
        default=False
    )
    transfer_home = models.BooleanField(
        'Мне нужен трансфер до дома',
        default=False
    )
    transfer_address = models.CharField(
        'Адрес трансфера (до дома)',
        max_length=500,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Ответ гостя'
        verbose_name_plural = 'Ответы гостей'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.fio} ({"придёт" if self.will_attend else "не придёт"})'
