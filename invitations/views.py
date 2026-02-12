"""
Представления для приглашения.
"""

import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods

from .forms import GuestResponseForm


# Константы для фронта
EVENT_DESCRIPTION = """
Мы рады пригласить вас на наше торжество! Этот день особенный для нас, 
и нам очень важно разделить его с близкими людьми. Ждём вас!
"""

PLAN_OF_DAY = [
    {'time': '14:30', 'title': 'Трансфер из Самары', 'description': 'Точка сбора будет указана позже', 'icon': 'bus-front'},
    {'time': '15:30', 'title': 'Сбор гостей', 'description': 'Встреча, welcome-коктейль', 'icon': 'people'},
    {'time': '16:00', 'title': 'Церемония', 'description': 'Начало торжественной церемонии', 'icon': 'heart'},
    {'time': '17:00', 'title': 'Банкет', 'description': 'Праздничный ужин', 'icon': 'cake'},
    {'time': '22:00–23:00', 'title': 'Окончание банкета', 'description': 'Прощание с гостями', 'icon': 'music-note-beamed'},
    {'time': '23:00', 'title': 'Обратный трансфер до Самары', 'description': 'Точки будут указаны позже', 'icon': 'bus-front'},
]

LOCATION_DESCRIPTION = """
Наше торжество состоится на живописной базе отдыха. 
Уютная атмосфера, красивая природа и тёплый приём ждут вас!
"""

LOCATION_ADDRESS = 'База отдыха «Циолковский»'
LOCATION_MAPS_LINK = 'https://yandex.ru/maps/?ll=50.298914%2C53.537715&mode=poi&poi%5Bpoint%5D=50.304565%2C53.542512&poi%5Buri%5D=ymapsbm1%3A%2F%2Forg%3Foid%3D36751272332&z=14'

DRESS_CODE_DESCRIPTION = 'Мы не строги к дресс-коду — просто поделимся идеей! Будем рады, если нашёлся наряд в нашей палитре цветов, но главное — ваше присутствие.'


def get_details():
    """Детали мероприятия для секции «Детали»."""
    return [
        {'title': 'Парковка', 'description': 'На территории базы отдыха предусмотрена бесплатная парковка для гостей.', 'icon': 'car-front'},
        {'title': 'Букеты', 'description': 'Букеты, к сожалению, быстро завянут, а мы, возможно, отправимся в путешествие и не успеем ими насладиться. Будем благодарны за альтернативу — бутылочку вина или другой напиток с запиской, к какому событию предлагаете приурочить её открытие. Также можете подарить хорошую книгу.', 'icon': 'flower1'},
        {'title': 'Ночевка', 'description': 'Арендуемые нами домики на базе отдыха рассчитаны на гостей из дальних городов. Если вы очень хотите остаться с ночёвкой, пожалуйста, укажите это в анкете ниже — мы подумаем, что можем для вас придумать.', 'icon': 'house'},
        {'title': 'Дети', 'description': 'На базе отдыха, к сожалению, нет детских зон и аниматоров для наших маленьких гостей. Пожалуйста, заранее подумайте, с кем оставить ваших крошек на время праздничного вечера.', 'icon': 'person'},
        {'title': 'Вопросы', 'description': 'Если в день мероприятия появятся вопросы, вы потеряетесь или готовите нам сюрприз — обращайтесь к нашему координатору.', 'icon': 'telephone'},
    ]


@ensure_csrf_cookie
def invitation_page(request):
    """Главная страница приглашения."""
    form = GuestResponseForm()
    context = {
        'form': form,
        'event_date': '12.09.2026',
        'event_datetime': '2026-09-12T15:30:00',
        'event_description': EVENT_DESCRIPTION.strip(),
        'plan_of_day': PLAN_OF_DAY,
        'location_description': LOCATION_DESCRIPTION.strip(),
        'location_address': LOCATION_ADDRESS,
        'location_maps_link': LOCATION_MAPS_LINK,
        'details': get_details(),
        'dress_code_description': DRESS_CODE_DESCRIPTION,
    }
    return render(request, 'invitation.html', context)


@require_http_methods(['POST'])
def submit_invitation(request):
    """API для отправки анкеты приглашения."""
    if request.content_type == 'application/json':
        data = json.loads(request.body)
        if 'alcohol_preferences' not in data:
            data['alcohol_preferences'] = []
        if 'non_alcohol_preferences' not in data:
            data['non_alcohol_preferences'] = []
        # ChoiceField ожидает ровно строку 'true' или 'false'
        val = data.get('will_attend')
        if val in (True, 'true', 'True', '1'):
            data['will_attend'] = 'true'
        else:
            data['will_attend'] = 'false'
        form = GuestResponseForm(data)
    else:
        form = GuestResponseForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True, 'message': 'Спасибо! Ваш ответ сохранён.'})
    return JsonResponse(
        {'success': False, 'errors': form.errors},
        status=400
    )
