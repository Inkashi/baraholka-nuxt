#!/bin/sh

# Ждём БД
echo "⏳ Waiting for MySQL (db:3306)..."
while ! nc -z db 3306; do
  sleep 1
done
echo "✅ MySQL is ready!"

# Выполняем миграции
echo "🚀 Applying migrations..."
python manage.py migrate --noinput

# Запускаем основную команду (например, runserver)
# "$@" — это то, что передано в CMD из Dockerfile
exec "$@"