from django.urls import path

from trading.api.views import TradeHistoryView


urlpatterns = [
    path('history/', TradeHistoryView.as_view(), name='trade-history'),
]
