from server.apps.flow_wallet.models import Job
from server.apps.flow_wallet.utils import convert_dict


class JobUpdater:
    def __init__(self, params):
        self.params = convert_dict(params)

    def do(self) -> Job:
        job_id = self.params.pop('job_id')
        errors = self.params.pop('errors', [])

        Job.objects.filter(id=job_id).update(
            **self.params,
            **{'errors': errors} if errors else {},
        )
        return Job.objects.get(id=job_id)

