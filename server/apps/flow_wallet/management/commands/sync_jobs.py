import traceback
from time import sleep

from django.core.management.base import BaseCommand, CommandError

from server.apps.flow_wallet.models import Job, Log
from server.apps.flow_wallet.server_api import FlowWalletServerAPI
from server.apps.flow_wallet.service.job_updater import JobUpdater


class Command(BaseCommand):
    help = 'Sync jobs with flow wallet API'

    def handle(self, *args, **options):
        while True:
            try:
                self.task()
            except Exception:
                exp = traceback.format_exc()
                Log.save_log(_type=Log.Type.UNDEFINED, request_data={'type': 'background task'}, response_data={
                    'traceback': exp,
                })
                self.stdout.write(self.style.ERROR('Some exception...'))

            finally:
                self.stdout.write(self.style.SUCCESS('sleeping...'))
                sleep(30)

                self.handle()

    def task(self):
        for job in Job.objects.exclude(state__in=[
            Job.State.ERROR,
            Job.State.COMPLETE,
            Job.State.FAILED,
        ]).all():
            api = FlowWalletServerAPI()

            preview_status = job.state

            job = JobUpdater(api.job.get(job.id)).do()

            if job.state != Job.State.INIT:
                Log.save_log(
                    _type=Log.Type.JOB_STATUS_UPDATED,
                    request_data={
                        'job_id': str(job.id),
                        'preview_status': preview_status,
                    },
                    response_data={
                        'new_status': job.state,
                    }
                )
                self.stdout.write(self.style.SUCCESS('Job "%s" changed' % job.pk))
