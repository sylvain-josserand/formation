from django.shortcuts import render

from django.views.generic import ListView, DetailView


from core.models import Transaction

# Create your views here.

class TransactionListView(ListView):
    model = Transaction


class TransactionDetailView(DetailView):
    model = Transaction
