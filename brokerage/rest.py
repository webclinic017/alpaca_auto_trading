import json
import pprint
import requests
from requests.exceptions import HTTPError
import logging
import time
import os
from .common import URL
import sseclient
from threading import Thread
from . import vars


logger = logging.getLogger(__name__)


class RetryException(Exception):
    pass


class APIError(Exception):
    """
    Represent API related error.
    error.status_code will have http status code.
    """

    def __init__(self, error, http_error=None):
        super().__init__(error['message'])
        self._error = error
        self._http_error = http_error
        

    @property
    def code(self):
        return self._error['code']

    @property
    def status_code(self):
        http_error = self._http_error
        if http_error is not None and hasattr(http_error, 'response'):
            return http_error.response.status_code

    @property
    def request(self):
        if self._http_error is not None:
            return self._http_error.request

    @property
    def response(self):
        if self._http_error is not None:
            return self._http_error.response
class ConnectionBroker:
    _base_url = 'https://broker-api.sandbox.alpaca.markets'
    
    def __init__(self):
        self._auth =(vars.BROKER_KEY, vars.BROKER_SECRET)
        self._session = requests.Session()
        self._session.auth = self._auth
        self._retry = int(os.environ.get('APCA_RETRY_MAX', 3))
        self._retry_wait = int(os.environ.get('APCA_RETRY_WAIT', 3))
        self._retry_codes = [int(o) for o in os.environ.get(
            'APCA_RETRY_CODES', '429,504').split(',')]
    
    def _request(self,
                 method,
                 path,
                 data=None,
                 base_url=None,
                 ):
        base_url = base_url or self._base_url
        url=(base_url + '/' + path)
        opts = {
            'allow_redirects': False
        }
        if method.upper() in ['GET', 'DELETE']:
            opts['params'] = data
        else:
            opts['json'] = data

        retry = self._retry
        if retry < 0:
            retry = 0
        while retry >= 0:
            try:
                return self._one_request(method, url, opts, retry)
            except RetryException:
                retry_wait = self._retry_wait
                logger.warning(
                    'sleep {} seconds and retrying {} '
                    '{} more time(s)...'.format(
                        retry_wait, url, retry))
                time.sleep(retry_wait)
                retry -= 1
                continue

    def _one_request(self, method: str, url: URL, opts: dict, retry: int):
        """
        Perform one request, possibly raising RetryException in the case
        the response is 429. Otherwise, if error text contain "code" string,
        then it decodes to json object and returns APIError.
        Returns the body json in the 200 status.
        """
        retry_codes = self._retry_codes
        resp = self._session.request(method, url, **opts)
        try:
            resp.raise_for_status()
        except HTTPError as http_error:
            # retry if we hit Rate Limit
            if resp.status_code in retry_codes and retry > 0:
                raise RetryException()
            if 'code' in resp.text:
                error = resp.json()
                if 'code' in error:
                    raise APIError(error, http_error)
            else:
                raise
        if resp.text != '':
            return resp.json()
        return None

    def get(self, path, data=None):
        return self._request('GET', path, data)

    def post(self, path, data=None):
        return self._request('POST', path, data)

    def put(self, path, data=None):
        return self._request('PUT', path, data)

    def patch(self, path, data=None):
        return self._request('PATCH', path, data)

    def delete(self, path, data=None):
        return self._request('DELETE', path, data)

    def is_open(self):
        resp =self.get('v1/clock')
        return resp['is_open']

class MarketData(ConnectionBroker):
    _base_url ='https://data.sandbox.alpaca.markets'
    
    def get_quote(self,symbol:str):
        return self.get(f'v2/stocks/{symbol}/quotes/latest')
class Broker(ConnectionBroker):        

    
    def create_account(self,data):
        resp = self.post('v1/accounts',data)
        return resp
    
    
    def get_account(self,account_id):
        """Get the account"""
        resp = self.get(f'v1/accounts/{account_id}')
        return resp
    
    def get_trading_account(self,account_id):
        
        resp = self.get(f'v1/trading/accounts/{account_id}/account')
        return resp
    
    def get_transfer_data_all(self,account_id):
        resp = self.get(f'v1/accounts/{account_id}/transfers')
        return resp
    
    def delete_transfer_data_id(self,account_id,transfer_id):
        resp = self.delete(f'v1/accounts/{account_id}/transfers/{transfer_id}')
        return resp
    
    def create_clearing_house_relationship(self,account_id:str,data:dict):
        resp = self.post(f'v1/accounts/{account_id}/ach_relationships',data)
        return resp
    
    def get_related_clearing_house(self,account_id):
        return self.get(f'v1/accounts/{account_id}/ach_relationships')
    
    
    def deposit_account(self,to_account:str,amount:str):
        clearing=self.get_related_clearing_house(to_account)
        clearing_id = clearing[0].get('id')
        resp = self.transfer_fund(to_account,clearing_id,'INCOMING',amount)
        return resp
    
    def transfer(self,from_account,to_account,amount):
        data = {
            "from_account": from_account,
            "entry_type": "JNLC",
            "to_account": to_account,
            "amount": amount,
            "description": "test text /fixtures/status=rejected/fixtures/"
        }
        
        return self.post(f'v1/journals',data)
    
    def close_position(self,account_id:str,symbol:str):
        resp = self.delete(f'v1/trading/accounts/{account_id}/positions/{symbol}')
        return resp
    
    def create_order_with_setup(self,account_id:str,symbol:str,qty:float,limit_price:float,take_profit:float,stop_loss:float):
        data ={}
        data['symbol'] =symbol
        data['side']='buy'
        data['qty'] =qty
        data['type'] ='limit'
        data['time_in_force'] ='gtc'
        data['limit_price'] =limit_price
        data['commission']=0.85
        if take_profit:
            data['order_class'] ='bracket'
            data['take_profit'] ={'limit_price':take_profit}
        if stop_loss:
            data['order_class'] ='bracket'
            data['stop_loss'] ={'limit_price':stop_loss,'stop_price':stop_loss}
        resp = self.submit_order(account_id,data)
        return resp
    
    def buy_order_direct(self,account_id:str,symbol:str,qty:float):
        data ={}
        data['symbol'] =symbol
        data['side']='buy'
        data['qty'] =qty
        data['type'] ='market'
        data['time_in_force'] ='day'
        resp = self.submit_order(account_id,data)
        return resp
    
    def sell_order_direct(self,account_id:str,symbol:str,qty:float):
        data ={}
        data['symbol'] =symbol
        data['side']='sell'
        data['time_in_force'] ='day'
        data['qty'] =qty
        data['type'] ='market'
        resp = self.submit_order(account_id,data)
        return resp
        
    def buy_order_limit(self,account_id:str,symbol:str,qty:float,limit_price:float):
        data ={}
        data['symbol'] =symbol
        data['side']='buy'
        data['qty'] =qty
        data['type'] ='limit'
        data['time_in_force'] ='gtc'
        data['limit_price'] =limit_price
        resp = self.submit_order(account_id,data)
        return resp
    
    def sell_order_limit(self,account_id:str,symbol:str,qty:float,limit_price:float):
        data ={}
        data['symbol'] =symbol
        data['side']='sell'
        data['qty'] =qty
        data['type'] ='limit'
        data['time_in_force'] ='gtc'
        data['limit_price'] =limit_price
        resp = self.submit_order(account_id,data)
        return resp
        
        
    
    def submit_order(self,account_id:str,data:dict):
        resp = self.post(f'v1/trading/accounts/{account_id}/orders',data)
        return resp
    
    
    def transfer_fund(self,account_id:str,ach_id:str,direction:str,amount:str):
        data={}
        data['transfer_type'] = 'ach'
        data['relationship_id'] = ach_id
        data['direction'] = direction
        data['amount'] = amount
        
        resp = self.post(f'v1/accounts/{account_id}/transfers',data)
        return resp
    
    
class BrokerEvents(ConnectionBroker):
    
    
    def _request(self,
                 method,
                 path,
                 data=None,
                 base_url=None,
                 ):
        base_url = base_url or self._base_url
        url=(base_url + '/' + path)
        headers = {'Accept': 'text/event-stream'}
        opts = {
            'stream': True,
            'headers':headers,
            "auth": self._auth
        }
        if method.upper() in ['GET', 'DELETE']:
            opts['params'] = data
        else:
            opts['json'] = data

        retry = self._retry
        if retry < 0:
            retry = 0
        while retry >= 0:
            try:
                return self.stream_request( url, opts)
            except RetryException:
                retry_wait = self._retry_wait
                logger.warning(
                    'sleep {} seconds and retrying {} '
                    '{} more time(s)...'.format(
                        retry_wait, url, retry))
                time.sleep(retry_wait)
                retry -= 1
                continue
    
    def stream_request(self,url, opts):
        response = requests.get(url, **opts)
        return response
    
    
    def stream_account_events(self):
        response = self.get('v1/events/accounts/status')
        client = sseclient.SSEClient(response)
        for event in client.events():
            pprint.pprint(json.loads(event.data))
    
    def stream_journal_events(self):
        response = self.get('v1/events/journals/status')
        client = sseclient.SSEClient(response)
        for event in client.events():
            pprint.pprint(json.loads(event.data))
    
    def stream_trade_events(self):
        response = self.get('v1/events/trades')
        client = sseclient.SSEClient(response)
        for event in client.events():
            pprint.pprint(json.loads(event.data))
            
            
    def stream_transfer_events(self):
        response = self.get('v1/events/transfers/status')
        client = sseclient.SSEClient(response)
        for event in client.events():
            pprint.pprint(json.loads(event.data))
    
    def stream_all_events(self):
        # Start all threads. 
        threads = [
            Thread(target=self.stream_account_events, daemon=True),
            Thread(target=self.stream_transfer_events, daemon=True),
            Thread(target=self.stream_journal_events, daemon=True),
            Thread(target=self.stream_trade_events, daemon=True),
        ]
        for event in threads:
            event.start()

        # Wait all threads to finish.
        for event in threads:
            event.join()