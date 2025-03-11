import json
import pytest

from unittest.mock import AsyncMock, patch
from channels.testing import WebsocketCommunicator

from rest_framework.test import APIClient
from django.core.cache import cache
from django.utils.timezone import now, timedelta

from config.asgi import application
from trading.models import Trade
from trading.consumers import BinanceConsumer


@pytest.mark.django_db
def test_trade_history():
    """Тест REST API истории торгов с проверкой кеша"""
    cache_key = 'trade_history'
    Trade.objects.create(symbol='BTC/USDT', price=50000, timestamp=now())
    cache.delete(cache_key)

    client = APIClient()
    response = client.get('/api/history/')

    assert response.status_code == 200
    assert len(response.data) == 1

    cached_data = cache.get(cache_key)
    assert cached_data is not None
    assert len(cached_data) == 1
    assert cached_data[0].symbol == 'BTC/USDT'


@pytest.mark.asyncio
async def test_websocket_connection():
    """Тест WebSocket-соединения"""

    communicator = WebsocketCommunicator(application, 'ws/trades/')
    connected, _ = await communicator.connect()
    assert connected
    await communicator.disconnect()


@pytest.mark.django_db
def test_trade_data_cleanup():
    """Тест очистки старых данных"""
    old_trade = Trade.objects.create(symbol='BTC/USDT', price=50000, timestamp=now() - timedelta(days=8))
    recent_trade = Trade.objects.create(symbol='ETH/USDT', price=3500, timestamp=now())

    Trade.clean_old_data(days=7)

    assert Trade.objects.filter(id=old_trade.id).count() == 0
    assert Trade.objects.filter(id=recent_trade.id).count() == 1


@pytest.mark.asyncio
@patch('websockets.connect', new_callable=AsyncMock)
async def test_fetch_binance_data(mock_ws_connect):
    """Тест обработки сообщений Binance"""

    mock_ws = AsyncMock()
    mock_ws.recv = AsyncMock(side_effect=[
        json.dumps({"s": "BTCUSDT", "p": "50000.0"}),
        json.dumps({"s": "ETHUSDT", "p": "3500.0"})
    ])
    mock_ws_connect.return_value.__aenter__.return_value = mock_ws

    consumer = BinanceConsumer()
    await consumer.fetch_binance_data()

    assert mock_ws.recv.call_count == 2


@pytest.mark.django_db
def test_trade_model_str():
    """Тест строкового представления модели Trade"""

    trade = Trade.objects.create(symbol='BTC/USDT', price=50000, timestamp=now())
    assert str(trade) == 'BTC/USDT - 50000.00000000'
