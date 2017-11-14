from django.contrib import admin
from core.models import Transaction


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'created', 'modified', 'label', 'initial_amount', 'initial_currency', 'active']

admin.site.register(Transaction, TransactionAdmin)
