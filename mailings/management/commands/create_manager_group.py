from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Создаёт группу "Менеджеры" и добавляет права на просмотр всех клиентов, сообщений и рассылок.'

    def handle(self, *args, **kwargs):
        group_name = 'Менеджеры'
        group, created = Group.objects.get_or_create(name=group_name)

        permissions = [
            Permission.objects.get(codename='can_view_all_clients'),
            Permission.objects.get(codename='can_view_all_messages'),
            Permission.objects.get(codename='can_view_all_mailings'),
        ]

        for perm in permissions:
            group.permissions.add(perm)

        if created:
            self.stdout.write(self.style.SUCCESS(f'Группа "{group_name}" успешно создана и права добавлены.'))
        else:
            self.stdout.write(self.style.WARNING(f'Группа "{group_name}" уже существует. Права обновлены.'))
