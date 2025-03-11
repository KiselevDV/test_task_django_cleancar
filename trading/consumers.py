import asyncio
import json
import logging
import websockets

from channels.generic.websocket import AsyncWebsocketConsumer
from datetime import datetime, timedelta
from django.core.cache import cache

from trading.tasks import save_trade


logger = logging.getLogger(__name__)


class BinanceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Подключение клиента к WebSocket"""
        await self.accept()
        await self.channel_layer.group_add('trades', self.channel_name)
        self.trading_pairs = ['btcusdt', 'ethusdt']
        self.last_saved = {}
        asyncio.create_task(self.fetch_binance_data())

    async def disconnect(self, close_code):
        """Отключение клиента"""
        await self.channel_layer.group_discard('trades', self.channel_name)

    async def fetch_binance_data(self):
        """Подключение к Binance с повторным подключением"""
        while True:
            try:
                url = 'wss://stream.binance.com:9443/ws/btcusdt@trade'
                async with websockets.connect(url) as ws:
                    logger.info(f'Подключен к Binance WebSocket: {url}')
                    while True:
                        data = json.loads(await ws.recv())
                        logger.debug(f'Получены данные: {data}')

                        symbol = data.get('s', '').lower()
                        price = float(data.get('p', 0))
                        now_time = datetime.utcnow()

                        last_time = self.last_saved.get(symbol, now_time - timedelta(minutes=1))
                        if (now_time - last_time).seconds >= 60:
                            save_trade.delay(symbol, price)
                            cache.delete('trade_history')
                            self.last_saved[symbol] = now_time
                            logger.info(f'Сохранена сделка {symbol}: {price}')

                        await self.channel_layer.group_send(
                            'trades',
                            {
                                'type': 'send_trade_update',
                                'symbol': symbol,
                                'price': price,
                                'timestamp': now_time.isoformat(),
                            }
                        )
            except Exception as e:
                logger.error(f'Ошибка WebSocket: {e}. Переподключение через 5 секунд...')
                await asyncio.sleep(5)

    async def send_trade_update(self, event):
        """Отправка данных клиентам"""
        await self.send(json.dumps(event))
