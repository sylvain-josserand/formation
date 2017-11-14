from django.contrib import admin
from core.models import Transaction


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'created', 'modified', 'owner', 'label', 'initial_amount', 'initial_currency', 'active']
    list_filter = ['owner__username', ]

admin.site.register(Transaction, TransactionAdmin)
