# Random Weather

Учебный веб-проект на Flask, который показывает погоду для случайного города.
Приложение получает случайный город, определяет его координаты и запрашивает текущую погоду через Open-Meteo. 

## Возможности
- получение погоды для случайного города;
- отображение температуры, скорости ветра и погодного состояния;
- история просмотренных городов;
- добавление городов в избранное;
- удаление городов из избранного;
- REST API;
- PostgreSQL;
- миграции базы данных через Alembic;
- автоматические тесты через pytest;
- проверка кода через Ruff;
- запуск приложения через Docker Compose.

## Стек

- Python 3.12
- Flask
- SQLAlchemy
- PostgreSQL
- Alembic
- Requests
- JavaScript
- HTML / CSS
- pytest
- Ruff
- Docker / Docker Compose

## API
### GET /api/weather

Получает погоду для случайного города и сохраняет результат в историю.

### GET /api/history

Возвращает последние записи истории.

### GET /api/favorites

Возвращает список избранных городов.

### POST /api/favorites

Добавляет город в избранное.

Пример запроса:

{
  "city": "London",
  "country": "United Kingdom",
  "latitude": 51.5074,
  "longitude": -0.1278
}

### DELETE /api/favorites/<favorite_id>

Удаляет город из избранного.

### GET /about

Простой информационный endpoint.

## Локальный запуск

### Создайте виртуальное окружение:

python -m venv .venv

### Активируйте его:

source .venv/Scripts/activate

### Установите зависимости:

pip install -r requirements-dev.txt

### Создайте .env с DATABASE_URL, затем запустите миграции:

alembic upgrade head

### Запуск приложения:

flask --app app run

##Тесты

### Запуск всех тестов:

pytest

### Проверка кода:

ruff check .

## Внешние API

Проект использует:

- Random City API — получение случайного города;
- Open-Meteo Geocoding API — получение координат города;
- Open-Meteo Forecast API — получение текущей погоды.

## Цель проекта

Проект создан для практики Flask, REST API, работы с PostgreSQL и SQLAlchemy, внешними API, тестированием и контейнеризацией Docker.
