# SneakerShop

Короткий гайд по локальній розробці та розгортанню

## Швидкий старт

1. Встановіть залежності

```bash
pip install -r requirements.txt
```

2. Налаштуйте змінні оточення (опційно)

- `SECRET_KEY` — секрет для сесій
- `ADMIN_PASSWORD` — пароль для адмін-панелі
- `ADMIN_TOKEN` — токен для API-адмін операцій

3. Ініціалізуйте БД і засійте прикладні дані

```bash
python -c "from models import init_db; init_db()"
python scripts/seed_products.py
```

4. Запустіть локально

```bash
FLASK_DEBUG=1 python app.py
```

5. Тести

```bash
pytest
```

## Розгортання у production

- Використовуйте Gunicorn + Nginx, встановіть `ADMIN_TOKEN` та `SECRET_KEY` у середовищі.
- Приклад запуску:

```bash
gunicorn -b 0.0.0.0:8000 app:app
```

## Далі

Заплановано:
- додати аутентифікацію користувачів, корзину покупок та інтеграцію платежів
- розширити тестове покриття
- додати CI/CD
