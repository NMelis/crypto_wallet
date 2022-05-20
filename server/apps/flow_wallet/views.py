from rest_framework import viewsets
from rest_framework.response import Response

from server.apps.flow_wallet.server_api import FlowWalletServerAPI
from server.apps.flow_wallet.service.job_create import JobCreator


class AccountViewSet(viewsets.ViewSet):
    """
    A ViewSet for listing or retrieving accounts.
    """

    def create(self, request):
        api = FlowWalletServerAPI()
        flow_wallet_job = api.account.create()
        job = JobCreator(flow_wallet_job).do()

        return Response({"id": job.pk})

    def list(self, request):
        api = FlowWalletServerAPI()
        return Response(api.account.get_all())

    def retrieve(self, request, pk):
        api = FlowWalletServerAPI()
        return Response(api.account.get(pk))
