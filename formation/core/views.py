from django.shortcuts import render
from django.views.generic import ListView
from core.models import Transaction


class TransactionListView(ListView):
    model = Transaction