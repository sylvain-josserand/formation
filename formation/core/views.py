from django.shortcuts import render
from django.views.generic import ListView
from core.models import Transaction

# Create your views here.

class TransactionListView(ListView):
    model = Transaction