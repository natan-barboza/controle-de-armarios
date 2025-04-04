#!/bin/sh

# Aguarda o banco de dados ficar disponível
echo "Esperando o banco de dados ficar pronto..."

while ! nc -z "$DB_HOST" 5432; do
  sleep 1
done

echo "Banco de dados disponível. Executando migrações e criando superusuário..."

python manage.py migrate
python apps/base/scripts/create_superuser.py

echo "Iniciando o Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 --workers 3 core.wsgi:application
