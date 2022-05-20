from server.apps.flow_wallet.models import Job
from server.apps.flow_wallet.utils import convert_dict


class JobCreator:
    def __init__(self, params):
        self.params = convert_dict(params)

    def do(self) -> Job:
        job_id = self.params.pop('job_id')
        errors = self.params.pop('errors', [])

        job = Job(
            id=job_id,
            **self.params,
        )
        if errors:
            job.errors = errors
        job.save()

        return job
