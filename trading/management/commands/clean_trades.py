from django.core.management.base import BaseCommand

from trading.models import Trade


class Command(BaseCommand):
    help = 'Удалить данные старше 7 дней'

    def handle(self, *args, **kwargs):
        Trade.clean_old_data()
        self.stdout.write(self.style.SUCCESS('Данные старше 7 дней удалены'))
