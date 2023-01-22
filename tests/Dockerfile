# Базовый образ
FROM python:3.10-slim

# Рабочая директория
WORKDIR /usr/src

# Настройка окружения
ARG APP_PORT=8004

ENV APP_PORT="${APP_PORT}"

# Установка зависимостей для python
COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

# Копируем проект
COPY . .

# start
CMD ["pytest", "-v", "./test_api.py"]
