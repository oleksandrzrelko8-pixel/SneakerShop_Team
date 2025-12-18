# Етап 1: Збірка (Builder)
<<<<<<< HEAD
FROM python:3.11-slim as builder

WORKDIR /app

# Встановлюємо залежності
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Етап 2: Фінальний образ (ЗМІНЮЄМО НА SLIM!)
FROM python:3.11-slim
=======
FROM python:3.9-slim as builder

WORKDIR /app

# Встановлюємо залежності, щоб не тягнути компілятор у фінальний образ
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Етап 2: Фінальний образ (Production)
FROM python:3.9-alpine
>>>>>>> 5e71a5a568c516fee2e693d7c1498a9dab5e7604

WORKDIR /app

# Копіюємо встановлені бібліотеки з першого етапу
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

<<<<<<< HEAD
# Встановлюємо wget для healthcheck
RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*

# Створюємо папку для бази даних
=======
# Створюємо папку для бази даних (це важливо для SQLite!)
>>>>>>> 5e71a5a568c516fee2e693d7c1498a9dab5e7604
RUN mkdir -p /app/data

# Копіюємо код проєкту
COPY . .

<<<<<<< HEAD
# Налаштування
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Порт
EXPOSE 5000

# Запуск
CMD ["python", "app.py"]
=======
# Налаштування змінних середовища
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Відкриваємо порт
EXPOSE 5000

# Команда запуску
CMD ["python", "app.py"]
>>>>>>> 5e71a5a568c516fee2e693d7c1498a9dab5e7604
