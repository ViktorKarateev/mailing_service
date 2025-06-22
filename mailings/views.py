from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Client
from .mixins import OwnerAccessMixin


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'mailings/client_list.html'

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)


class ClientDetailView(OwnerAccessMixin, DetailView):
    model = Client
    template_name = 'mailings/client_detail.html'


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = ['email', 'full_name', 'comment']
    template_name = 'mailings/client_form.html'
    success_url = reverse_lazy('mailings:client_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientUpdateView(OwnerAccessMixin, UpdateView):
    model = Client
    fields = ['email', 'full_name', 'comment']
    template_name = 'mailings/client_form.html'
    success_url = reverse_lazy('mailings:client_list')


class ClientDeleteView(OwnerAccessMixin, DeleteView):
    model = Client
    template_name = 'mailings/client_confirm_delete.html'
    success_url = reverse_lazy('mailings:client_list')
