# Используем базовый образ Python 3.9 slim
FROM python:3.9-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /finance_app

# Копируем файл с зависимостями в контейнер
COPY requirements.txt requirements.txt

# Обновляем pip и устанавливаем необходимые зависимости
RUN pip install --upgrade pip && pip install psycopg2-binary
RUN pip install -r requirements.txt

# Копируем все файлы приложения в контейнер
COPY . .

# Устанавливаем переменную окружения для Flask
ENV FLASK_APP=app.py

# Копируем и делаем исполняемым скрипт для запуска приложения
COPY entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh

# Открываем порт 5000 для доступа к приложению
EXPOSE 5000

# Указываем команду запуска контейнера
ENTRYPOINT ["./entrypoint.sh"]

