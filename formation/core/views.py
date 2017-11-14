from core.models import Transaction
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseRedirect
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
    success_url = '/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())