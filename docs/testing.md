# Тестирование

Проект использует `pytest`.
Запуск тестов:
```sh
docker-compose run web pytest
```

## Описание тестов
- `test_trade_history()` – проверяет API истории торгов и кеширование.
- `test_websocket_connection()` – тестирует подключение к WebSocket.
- `test_trade_data_cleanup()` – проверяет удаление устаревших записей.
- `test_fetch_binance_data()` – эмулирует получение данных от Binance через WebSocket.
- `test_trade_model_str()` – проверяет строковое представление модели `Trade`.

[Вернуться к README](../README.md)