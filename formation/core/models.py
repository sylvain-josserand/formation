from django.db import models
from decimal import Decimal


class MoneyField(models.DecimalField):
    def __init__(self, verbose_name=None, name=None, max_digits=None,
                 decimal_places=None, **kwargs):
        super(MoneyField, self).__init__(
            verbose_name=verbose_name,
            name=name,
            max_digits=10,
            decimal_places=2,
            **kwargs,
        )


class ActiveTransactionManager(models.Manager):
    def get_queryset(self):
        return super(ActiveTransactionManager, self).get_queryset().filter(active=True)


class DatedModel(models.Model):
    class Meta:
        abstract = True
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Transaction(DatedModel):
    label = models.CharField(max_length=100)
    initial_amount = MoneyField()
    initial_currency = models.CharField(
        max_length=3,
        choices=(
            ('EUR', 'Euro'),
            ('USD', 'Dollar US'),
            ('JPY', 'Yen'),
        ),
        default='EUR',
    )
    converted_amount = MoneyField(default=None, blank=True, null=True)
    active = models.BooleanField(default=True)

    activetransactions = ActiveTransactionManager()

    def save(self, *args, **kwargs):
        self.converted_amount = self.convert(from_=self.initial_currency, to='EUR', amount=self.initial_amount)
        super(Transaction, self).save(*args, **kwargs)

    @property
    def conversion_rate(self):
        if self.initial_amount == 0:
            raise Exception("Not possible to get the conversion rate when initial amount is zero!")
        return self.converted_amount/self.initial_amount

    def convert(self, from_, to, amount):
        if from_==to:
            return amount
        else:
            # Get conversion rates from fixer.io
            pass
