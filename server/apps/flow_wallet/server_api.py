import traceback
import uuid

import requests

from server.apps.flow_wallet.models import Log
from server.settings.components.flow_wallet_api import FLOW_WALLET_API


class BaseApi:
    def __init__(self, host):
        self.host = host

    def request(self, method, url, **kwargs):
        request_data = {
                'method': method,
                'url': url,
                **kwargs,
            }
        try:
            response = requests.request(method, url, **kwargs)
            Log.save_log(_type=Log.Type.REQUEST, request_data=request_data, response_data={
                'headers': dict(response.headers),
                'body': response.json()
            })
            return response
        except Exception as ex:
            Log.save_log(_type=Log.Type.UNDEFINED, request_data=request_data, response_data={
                'traceback': traceback.format_exc(),
            })
            raise ex


class AccountAPI(BaseApi):
    def create(self, **params):
        response = self.request('post', f'{self.host}/accounts', headers={
            'Idempotency-Key': params.get('key', uuid.uuid4().hex),
        })
        return response.json()

    def get(self, address):
        response = self.request('get', f'{self.host}/accounts/{address}')
        return response.json()

    def get_all(self):
        response = self.request('get', f'{self.host}/accounts')
        return response.json()


class JobAPI(BaseApi):
    def get(self, job_id):
        response = self.request('get', f'{self.host}/jobs/{job_id}')
        return response.json()


class FlowWalletServerAPI(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(FlowWalletServerAPI, cls).__new__(cls)
            cls.instance.host = FLOW_WALLET_API
            cls.instance.job = JobAPI(FLOW_WALLET_API)
            cls.instance.account = AccountAPI(FLOW_WALLET_API)
        return cls.instance

