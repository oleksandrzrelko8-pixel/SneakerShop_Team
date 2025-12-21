# Етап 1: Збірка (Builder)
FROM python:3.11-slim as builder

WORKDIR /app

# Встановлюємо залежності
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Етап 2: Фінальний образ
FROM python:3.11-slim

WORKDIR /app

# Копіюємо встановлені бібліотеки з першого етапу
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Встановлюємо wget для перевірки здоров'я контейнера (healthcheck)
RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*

# Створюємо папку для бази даних
RUN mkdir -p /app/data

# Копіюємо код проєкту
COPY . .

# Налаштування
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Порт
EXPOSE 5000

# Запуск
CMD ["python", "app.py"]