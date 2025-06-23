from typing import Any
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView )
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views import View
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from .mixins import OwnerAccessMixin
from .models import Message, Mailing, Attempt, Client
from .forms import MailingForm


class HomeView(TemplateView):
    template_name = 'mailings/home.html'

    def get_context_data(self, **kwargs: Any) -> dict:
        context = super().get_context_data(**kwargs)
        context['total_mailings'] = Mailing.objects.count()
        context['active_mailings'] = Mailing.objects.filter(status='launched').count()
        context['unique_clients'] = Client.objects.values('email').distinct().count()
        return context


# Клиенты
@method_decorator(cache_page(60 * 15), name='dispatch')
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


# Сообщения
@method_decorator(cache_page(60 * 15), name='dispatch')
class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'mailings/message_list.html'

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageDetailView(OwnerAccessMixin, DetailView):
    model = Message
    template_name = 'mailings/message_detail.html'


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ['subject', 'body']
    template_name = 'mailings/message_form.html'
    success_url = reverse_lazy('mailings:message_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(OwnerAccessMixin, UpdateView):
    model = Message
    fields = ['subject', 'body']
    template_name = 'mailings/message_form.html'
    success_url = reverse_lazy('mailings:message_list')


class MessageDeleteView(OwnerAccessMixin, DeleteView):
    model = Message
    template_name = 'mailings/message_confirm_delete.html'
    success_url = reverse_lazy('mailings:message_list')


# Рассылки
@method_decorator(cache_page(60 * 15), name='dispatch')
class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailings/mailing_list.html'

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


class MailingDetailView(OwnerAccessMixin, DetailView):
    model = Mailing
    template_name = 'mailings/mailing_detail.html'


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailings:mailing_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(OwnerAccessMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailings:mailing_list')


class MailingDeleteView(OwnerAccessMixin, DeleteView):
    model = Mailing
    template_name = 'mailings/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailings:mailing_list')


# Попытки рассылки
class AttemptListView(LoginRequiredMixin, ListView):
    model = Attempt
    template_name = 'mailings/attempt_list.html'

    def get_queryset(self):
        return Attempt.objects.filter(mailing__owner=self.request.user)


# Отправка рассылки
class SendMailingView(LoginRequiredMixin, View):
    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk, owner=request.user)
        subject = mailing.message.subject
        body = mailing.message.body
        success_count = 0
        fail_count = 0

        for client in mailing.clients.all():
            try:
                send_mail(
                    subject,
                    body,
                    request.user.email,
                    [client.email],
                    fail_silently=False,
                )
                Attempt.objects.create(
                    mailing=mailing,
                    status='Успешно',
                    server_response='OK',
                )
                success_count += 1
            except Exception as e:
                Attempt.objects.create(
                    mailing=mailing,
                    status='Не успешно',
                    server_response=str(e),
                )
                fail_count += 1

        messages.success(request, f'Успешно: {success_count}, Ошибок: {fail_count}')
        return redirect('mailings:mailing_detail', pk=mailing.pk)
