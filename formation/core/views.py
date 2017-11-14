from core.models import Transaction
from django.contrib.auth.models import AnonymousUser
from django.views.generic import ListView, DetailView, CreateView


class AuthMixin:
    def get_queryset(self):
        if not self.request.user or isinstance(self.request.user, AnonymousUser):
            return Transaction.objects.none()
        else:
            user = self.request.user
            queryset = super().get_queryset()
            if user.is_superuser:
                return queryset
            else:
                return queryset.filter(owner=user)


class TransactionListView(AuthMixin, ListView):
    model = Transaction


class TransactionDetailView(AuthMixin, DetailView):
    model = Transaction


class TransactionCreateView(AuthMixin, CreateView):
    model = Transaction
    fields = ['label', 'initial_amount', 'initial_currency']

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)