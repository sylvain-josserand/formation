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
        return super(ActiveTransactionManager, self).get_queryset().filter(actif=True)


class DatedModel(models.Model):
    class Meta:
        abstract = True
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Transaction(DatedModel):
    label = models.CharField(max_length=100)
    amount = MoneyField()
    active = models.BooleanField(default=True)
    activetransactions = ActiveTransactionManager()




    