from django.db import models

from django.utils.timezone import now, timedelta


class Trade(models.Model):
    symbol = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=18, decimal_places=8)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f'{self.symbol} - {self.price}'

    @staticmethod
    def clean_old_data(days=7):
        """Удаляет записи старше заданного количества дней (по умолчанию 7)"""

        threshold = now() - timedelta(days=days)
        Trade.objects.filter(timestamp__lt=threshold).delete()
