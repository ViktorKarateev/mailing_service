from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Client, Message, Mailing, MailingLog, Attempt


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'owner')
    search_fields = ('email', 'full_name')
    list_filter = ('owner',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'owner')
    search_fields = ('subject',)
    list_filter = ('owner',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'status', 'owner')
    list_filter = ('status', 'owner')


@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('attempt_time', 'status', 'mailing')
    list_filter = ('status', 'mailing')


def setup_manager_group():
    group, _ = Group.objects.get_or_create(name='Менеджеры')

    for model in [Client, Message, Mailing, Attempt]:
        content_type = ContentType.objects.get_for_model(model)
        permission = Permission.objects.filter(
            content_type=content_type,
            codename__startswith='can_view_all_'
        ).first()
        if permission:
            group.permissions.add(permission)


setup_manager_group()
