from django.urls import re_path
from trading.consumers import BinanceConsumer

websocket_urlpatterns = [
    re_path(r'ws/trades/$', BinanceConsumer.as_asgi()),
]
