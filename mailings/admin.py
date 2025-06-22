from django.contrib import admin
from .models import Client, Message, Mailing, MailingLog

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
