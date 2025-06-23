from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from mailings.models import Mailing, Attempt


class Command(BaseCommand):
    help = 'Отправка активных рассылок'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        active_mailings = Mailing.objects.filter(
            status='launched',
            start_time__lte=now,
            end_time__gte=now
        )

        for mailing in active_mailings:
            subject = mailing.message.subject
            body = mailing.message.body
            owner_email = mailing.owner.email

            for client in mailing.clients.all():
                # Исправленная проверка по клиенту
                already_sent = Attempt.objects.filter(
                    mailing=mailing,
                    timestamp__date=now.date(),
                    status='Успешно',
                    server_response='OK',
                ).filter(mailing__clients=client).exists()

                if already_sent:
                    self.stdout.write(f" {client.email} — уже отправлено сегодня, пропускаем.")
                    continue

                try:
                    send_mail(
                        subject,
                        body,
                        owner_email,
                        [client.email],
                        fail_silently=False
                    )
                    Attempt.objects.create(
                        mailing=mailing,
                        status='Успешно',
                        server_response='OK',
                    )
                    self.stdout.write(f" {client.email} — отправлено")
                except Exception as e:
                    Attempt.objects.create(
                        mailing=mailing,
                        status='Не успешно',
                        server_response=str(e),
                    )
                    self.stdout.write(f" {client.email} — ошибка: {e}")
