# 🛒 Software Shop

**Software Shop** — это веб-приложение на Django с Telegram-ботом для уведомлений о покупках и подписках. Проект включает полноценную админку, REST API, работу с PostgreSQL и асинхронным ботом на `python-telegram-bot`, разворачивается через `docker-compose`.

---

## 🚀 Возможности

- 🔐 JWT-аутентификация с `djoser`
- 📦 Управление товарами, вариантами, подписками и покупками
- 🤖 Асинхронный Telegram-бот, уведомляющий о покупках и подписках
- ⚙️ Админ-панель Django
- 🐘 PostgreSQL в контейнере
- 📄 Автозагрузка фикстур
- 💅 Линтинг с `isort` и `black`

---

## 🧰 Технологии

- Backend: Django 4+, DRF (Django REST Framework)
- Telegram Bot: [`python-telegram-bot`](https://github.com/python-telegram-bot/python-telegram-bot)
- База данных: PostgreSQL 17
- Docker & Docker Compose
- JWT-аутентификация (`djoser`)
- Python 3.12+

---

## 📦 Установка и запуск

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/olexasha/software_shop.git
cd software_shop
```

### 2. Переменные окружения
#### В docker-compose.yml укажите переменные окружения, главное токен вашего бота: `TG_BOT_TOKEN`

### 3. Запуск через Docker Compose
Убедитесь, что установлены Docker и Docker Compose.
```bash
docker-compose up -d
```

#### Все сервисы будут подняты:

`postgres` — база данных PostgreSQL

`migrations` — применение миграций

`fixtures` — загрузка фикстур

`app` — основной Django-сервер на localhost:8000

`tg_bot` — Telegram-бот

### 📂 Структура проекта
```bash
.
├── docker-compose.yaml
├── Dockerfile
├── pyproject.toml
├── README.md
├── requirements.txt
├── setup.cfg
└── software_shop
    ├── fixtures
    │   ├── products_product.json
    │   ├── products_productvariant.json
    │   ├── products_purchase.json
    │   ├── subscriptions_tariff.json
    │   ├── subscriptions_usersubscription.json
    │   └── users_customuser.json
    ├── __init__.py
    ├── manage.py
    ├── products
    │   ├── admin.py
    │   ├── apps.py
    │   ├── __init__.py
    │   ├── migrations
    │   │   
    │   ├── models.py
    │   ├── permissions.py
    │   ├── serializers.py
    │   ├── signals.py
    │   ├── urls.py
    │   └── views.py
    ├── software_shop
    │   ├── asgi.py
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── subscriptions
    │   ├── admin.py
    │   ├── apps.py
    │   ├── __init__.py
    │   ├── migrations
    │   │   ├── __init__.py
    │   ├── models.py
    │   ├── serializers.py
    │   ├── urls.py
    │   └── views.py
    ├── templates
    ├── users
    │   ├── admin.py
    │   ├── apps.py
    │   ├── __init__.py
    │   ├── migrations
    │   ├── models.py
    └── utils
        ├── has_subscription_middleware.py
        ├── __init__.py
        ├── tg_bot
        │   ├── bot.py
        │   ├── db.py
        │   ├── handlers.py
        │   ├── helpers.py
        │   ├── __init__.py
        └── upload_fixtures.sh
```

### 🧪 REST API

#### Продукты и покупки:
```bash
GET     /products/
POST    /products/
GET     /products/{id}/
PUT     /products/{id}/
DELETE  /products/{id}/

GET     /product/{product_pk}/variants/
POST    /product/{product_pk}/variants/
GET     /product/{product_pk}/variants/{pk}/
PATCH   /product/{product_pk}/variants/{pk}/
DELETE  /product/{product_pk}/variants/{pk}/

GET     /purchases/
POST    /purchases/
```

#### Подписки и тарифы:
```bash
GET     /tariffs/
GET     /subscription/
POST    /subscription/
```

#### Также доступны:

`admin/` — Django админка

`djoser/` — эндпоинты регистрации и логина

`djoser/jwt/` — эндпоинты получения и обновления JWT-токена

`djoser/password/reset/` — эндпоинты сброса пароля

`djoser/password/reset/confirm/` — эндпоинты подтверждения сброса пароля

`djoser/password/reset/complete/` — эндпоинты завершения сброса пароля

### 🧹 Линтинг
Проект использует следующие линтеры:

`black` — автоформатирование кода

`isort` — сортировка импортов

#### Запуск:
```bash
black .
isort .
```

### 📦 Фикстуры
После применения миграций автоматически загружаются фикстуры через сервис fixtures, который исполняет `utils/upload_fixtures.sh`.

### 🤖 Telegram-бот
Telegram-бот написан с использованием `python-telegram-bot`. Он асинхронно оповещает пользователей о следующих событиях:
- Покупка товара
- Подключение подписки


📬 Контакты
- Telegram: [@olexasha](https://t.me/olexasha)
- GitHub: [Olexasha](https://github.com/olexasha)