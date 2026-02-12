# Приглашение на свадьбу

Онлайн-приглашение с анкетой для гостей. Django + HTML/CSS/Bootstrap 5. PostgreSQL в Docker.

## Быстрый старт (Docker)

```bash
docker compose up --build
```

Приложение: http://localhost:8000  
Админка: http://localhost:8000/admin

### Первый запуск — создать суперпользователя

```bash
docker compose exec web python manage.py createsuperuser
```

## Локальная разработка (без Docker)

1. Создать виртуальное окружение и установить зависимости:
```bash
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

2. Запустить PostgreSQL (или использовать Docker только для БД):
```bash
docker compose up db -d
```

3. Миграции и сервер:
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Деплой на сервер

### 1. Проверка и установка Docker Compose

**Проверить, установлен ли Docker Compose:**
```bash
docker compose version
```
Если команда найдена и выводит версию — всё готово.

**Установка на Ubuntu/Debian:**

```bash
# Установка Docker (если ещё нет)
sudo apt update
sudo apt install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Добавить пользователя в группу docker (чтобы не писать sudo)
sudo usermod -aG docker $USER
# Выйдите и зайдите снова в SSH, чтобы группа применилась
```

**Проверка после установки:**
```bash
docker compose version
```

### 2. Клонирование и настройка

```bash
git clone <ваш-репозиторий> wedding-invitation
cd wedding-invitation
```

### 3. Переменные окружения

Создайте файл `.env` в корне проекта:

```env
POSTGRES_PASSWORD=ваш_надёжный_пароль
DJANGO_SECRET_KEY=сгенерируйте_случайную_строку_50_символов
ALLOWED_HOSTS=kirillandangelina.wedding.ru,www.kirillandangelina.wedding.ru,IP_ВАШЕГО_СЕРВЕРА
DJANGO_DEBUG=False
```

Сгенерировать `DJANGO_SECRET_KEY`:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**Важно:** в `ALLOWED_HOSTS` укажите ваш домен и IP сервера (через запятую, без пробелов).

### 4. Добавьте статику

Перед деплоем убедитесь, что в проекте есть:
- `static/images/1755076780159.jpg` — главное фото
- `static/images/palette.jpg` — палитра дресс-кода
- `static/images/map.png` — карта местности
- `static/audio/background.mp3` — фоновая музыка

### 5. Запуск

```bash
docker compose up -d --build
```

### 6. Создание суперпользователя (админка)

```bash
docker compose exec web python manage.py createsuperuser
```

Введите логин и пароль для входа в админку.

### 7. Домен и админка

**Да, админка будет доступна по адресу вида:**
- `http://kirillandangelina.wedding.ru/admin` (если приложение на порту 80)
- или `http://kirillandangelina.wedding.ru:8000/admin` (если на порту 8000)

**Что нужно сделать:**
1. Купить домен и привязать его к IP вашего сервера (A-запись в DNS).
2. Указать домен в `ALLOWED_HOSTS` (см. шаг 3).
3. Открыть порт 8000 в файрволе (если используете порт 8000):
   ```bash
   sudo ufw allow 8000
   sudo ufw enable
   ```

Приложение по умолчанию слушает порт 8000. Гости откроют `http://ваш-домен:8000`, админка — `http://ваш-домен:8000/admin`.

**Чтобы открывать сайт без :8000** (т.е. `http://ваш-домен`), в `docker-compose.yml` замените `"8000:8000"` на `"80:8000"` в секции `ports` сервиса `web`. Тогда откройте порт 80: `sudo ufw allow 80`.

### 8. Volumes (данные сохраняются)

В `docker-compose.yml` настроены тома:
- `postgres_data` — база данных (ответы гостей)
- `static_volume` — собранные статические файлы
- `media_volume` — загруженные файлы

При `docker compose down` данные не удаляются.

---

## Настройка контента

В `invitations/views.py` задайте:
- `EVENT_DESCRIPTION`, `PLAN_OF_DAY`, `get_details()`
- `LOCATION_DESCRIPTION`, `LOCATION_ADDRESS`, `LOCATION_MAPS_LINK`
- `DRESS_CODE_DESCRIPTION`

Файлы в `static/`:
- `images/1755076780159.jpg` — главное фото
- `images/palette.jpg` — палитра
- `images/map.png` — карта
- `audio/background.mp3` — музыка
