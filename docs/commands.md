# Базовые команды

## Остановка контейнеров
```bash
docker-compose down
```

## Просмотр логов
```bash
docker-compose logs -f web
```

## Перезапуск сервиса Celery
```bash
docker restart celery_worker_cleancar
```

## Очистка старых данных
Для удаления данных старше 7 дней используйте команду:
```sh
docker-compose run web python manage.py clean_trades
```

## Проверка flake8
```sh
docker compose exec web poetry run flake8 .
```

[Вернуться к README](../README.md)