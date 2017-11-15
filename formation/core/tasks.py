from core.models import Transaction


def update_currency_conversion(transaction_id):
    transaction = Transaction.objects.get(pk=transaction_id)
    amount = transaction.convert(transaction.initial_currency, 'USD', transaction.initial_amount)
    transaction.converted_amount = amount
    transaction.save()
    return amount
