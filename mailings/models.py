from django.db import models
from django.conf import settings


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name='Email')
    full_name = models.CharField(max_length=255, verbose_name='ФИО')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='clients',
        verbose_name='Владелец'
    )

    def __str__(self):
        return f"{self.full_name} <{self.email}>"

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name='Тема')
    body = models.TextField(verbose_name='Тело письма')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Владелец'
    )

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Mailing(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('launched', 'Запущена'),
        ('completed', 'Завершена'),
    ]

    start_time = models.DateTimeField(verbose_name='Время начала')
    end_time = models.DateTimeField(verbose_name='Время окончания')
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='created', verbose_name='Статус'
    )
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение')
    clients = models.ManyToManyField(Client, verbose_name='Клиенты')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mailings',
        verbose_name='Владелец'
    )

    def __str__(self):
        return f"Рассылка от {self.start_time} до {self.end_time}"

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MailingLog(models.Model):
    STATUS_CHOICES = [
        ('success', 'Успешно'),
        ('failed', 'Неуспешно'),
    ]

    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name='Время попытки')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='Статус')
    server_response = models.TextField(verbose_name='Ответ сервера')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка')

    def __str__(self):
        return f"[{self.get_status_display()}] {self.attempt_time}"

    class Meta:
        verbose_name = 'Лог рассылки'
        verbose_name_plural = 'Логи рассылок'


class Attempt(models.Model):
    mailing = models.ForeignKey('Mailing', on_delete=models.CASCADE, related_name='attempts', verbose_name='Рассылка')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время')
    status = models.CharField(max_length=100, verbose_name='Статус')
    server_response = models.TextField(blank=True, verbose_name='Ответ сервера')

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'

    def __str__(self):
        return f'Попытка от {self.timestamp} для {self.mailing}'