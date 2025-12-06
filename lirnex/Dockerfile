FROM python:3.12-slim-bullseye

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Установка зависимостей
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . /app/

# Сбор статических файлов
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Запуск gunicorn — ВАЖНО: правильный путь к wsgi
CMD ["gunicorn", "lirnex.wsgi:application", "-b", "0.0.0.0:8000"]
