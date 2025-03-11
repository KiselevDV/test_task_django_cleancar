import logging

from celery import shared_task
from django.utils.timezone import now


logger = logging.getLogger(__name__)


@shared_task
def save_trade(symbol, price):
    """Сохранение курса раз в минуту"""
    from trading.models import Trade
    try:
        Trade.objects.create(symbol=symbol, price=price, timestamp=now())
        logger.info(f'Сохранена сделка {symbol}: {price}')
    except Exception as e:
        logger.error(f'Ошибка при сохранении курса {symbol}: {e}')


@shared_task
def clean_old_trades():
    """Удаляет старые сделки (старше 14 дней)"""
    from trading.models import Trade
    Trade.clean_old_data(days=14)
    logger.info('Старые сделки удалены')
