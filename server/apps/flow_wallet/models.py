from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.fields.json import JSONField
from django.utils.translation import gettext_lazy as _


class Log(models.Model):
    class Type(models.IntegerChoices):
        UNDEFINED = 0, _('Undefined')
        REQUEST = 1, _('Request')
        JOB_CREATED = 2, _('Job is created')
        JOB_STATUS_UPDATED = 3, _('Job status is updated')
        ACCOUNT_CREATED = 4, _('Account is created')
        ACCOUNT_GET_ALL_REQUEST = 5, _('Request to get all accounts info')
        ACCOUNT_GET_REQUEST = 6, _('Request to get account info')

    request_data = JSONField(default={})
    response_data = JSONField(default={})
    type = models.SmallIntegerField(choices=Type.choices)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)

    @staticmethod
    def save_log(_type, request_data, response_data):
        Log.objects.create(
            type=_type,
            request_data=request_data,
            response_data=response_data,
        )


class Job(models.Model):
    class State(models.TextChoices):
        INIT = 'INIT', _('Init')
        ACCEPTED = 'ACCEPTED', _('Accepted')
        NO_AVAILABLE_WORKERS = 'NO_AVAILABLE_WORKERS', _('No available workers')
        ERROR = 'ERROR', _('Error')
        COMPLETE = 'COMPLETE', _('Complete')
        FAILED = 'FAILED', _('Failed')

    id = models.UUIDField(primary_key=True)
    type = models.CharField(_('Type'), max_length=512)
    state = models.CharField(max_length=24, choices=State.choices, default=State.INIT)
    error = models.CharField(_('Error'), max_length=512)
    errors = ArrayField(
            models.CharField(max_length=512, blank=True),
            size=256,
            default=[],
            verbose_name=_('Errors'),
        )
    result = models.CharField(_('Result'), max_length=512)
    transaction_id = models.CharField(_('Transaction id'), max_length=512)
    created_at = models.DateTimeField(_('Created at'))
    updated_at = models.DateTimeField(_('Updated at'))

    class Meta:
        verbose_name = _('Job')
        verbose_name_plural = _('Jobs')
