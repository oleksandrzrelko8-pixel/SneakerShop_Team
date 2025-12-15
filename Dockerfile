# Етап 1: Збірка (Builder)
FROM python:3.9-slim as builder

WORKDIR /app

# Встановлюємо залежності, щоб не тягнути компілятор у фінальний образ
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Етап 2: Фінальний образ (Production)
FROM python:3.9-alpine

WORKDIR /app

# Копіюємо встановлені бібліотеки з першого етапу
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Створюємо папку для бази даних (це важливо для SQLite!)
RUN mkdir -p /app/data

# Копіюємо код проєкту
COPY . .

# Налаштування змінних середовища
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Відкриваємо порт
EXPOSE 5000

# Команда запуску
CMD ["python", "app.py"]
