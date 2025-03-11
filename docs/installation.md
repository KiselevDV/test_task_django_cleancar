# Установка

## 1. Клонировать репозиторий
```bash
git clone https://github.com/KiselevDV/test_task_django_cleancar.git
cd test_task_django_cleancar
```

## 2. Установить зависимости через Poetry:
```bash
poetry install
```

## 3. Настройка переменных окружения
Создайте файл `.env` в корневой директории и добавьте:
```env
SECRET_KEY='my_secret_key'
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
POSTGRES_DB='test_database_cleancar'
POSTGRES_USER='test_user_cleancar'
POSTGRES_PASSWORD='test_password_cleancar'
POSTGRES_HOST='db_postgresql'
POSTGRES_PORT=5432
REDIS_HOST='redis'
REDIS_PORT=6379
CELERY_BROKER='redis://redis:6379/0'
```

## 4. Запуск проекта через Docker
```bash
cd docker
docker-compose up --build -d
```

## 5. Применение миграций
```bash
docker exec -it web_cleancar poetry run python manage.py migrate
```

## 6. Создание суперпользователя
```bash
docker exec -it web_cleancar poetry run python manage.py createsuperuser
```
[Вернуться к README](../README.md)