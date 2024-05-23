#!/bin/sh

# Прекратить выполнение скрипта при возникновении ошибки
set -e

# Инициализация базы данных, если она еще не инициализирована
flask db init || true

# Создание новой миграции базы данных с описанием "Initial migration"
flask db migrate -m "Initial migration" || true

# Применение миграций к базе данных
flask db upgrade || true

# Запуск приложения Flask на всех сетевых интерфейсах, порт 5000
exec flask run --host=0.0.0.0 --port=5000

