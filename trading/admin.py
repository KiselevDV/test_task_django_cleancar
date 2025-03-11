from django.contrib import admin

from trading.models import Trade


@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'price', 'timestamp')
    search_fields = ('symbol',)
    list_filter = ('symbol', 'timestamp')
    ordering = ('-timestamp',)
