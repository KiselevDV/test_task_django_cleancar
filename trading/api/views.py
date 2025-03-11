from django.core.cache import cache
from rest_framework import generics

from trading.api.serializers import TradeSerializer
from trading.models import Trade


class TradeHistoryView(generics.ListAPIView):
    serializer_class = TradeSerializer

    def get_queryset(self):
        cache_key = 'trade_history'
        data = cache.get(cache_key)
        if not data:
            data = Trade.objects.all().order_by('-timestamp')[:100]
            cache.set(cache_key, data, timeout=60)
        return data
