from django.contrib import admin

from server.apps.flow_wallet.models import Job, Log


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'state', 'error', 'result', 'transaction_id', 'created_at']


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ['type', 'request_data', 'created_at']
