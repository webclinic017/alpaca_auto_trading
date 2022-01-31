
import hashlib
import hmac
import json
from datetime import datetime
from requests.auth import AuthBase
import requests

URL = 'https://api.coinbase.com'

class Auth(AuthBase):
    VERSION = b'2021-03-30'

    def __init__(self, API_KEY, API_SECRET):
        self.API_KEY = API_KEY
        self.API_SECRET = API_SECRET

    def __call__(self, request):
        timestamp = datetime.now().strftime('%s')
        message = f"{timestamp}{request.method}{request.path_url}{request.body or ''}"
        signature = hmac.new(self.API_SECRET.encode(),
                             message.encode('utf-8'),
                             digestmod=hashlib.sha256)
        signature_hex = signature.hexdigest()

        request.headers.update({
            'CB-ACCESS-SIGN': signature_hex,
            'CB-ACCESS-TIMESTAMP': timestamp.encode(),
            'CB-ACCESS-KEY': self.API_KEY.encode(),
            'CB-VERSION': self.VERSION,
            'Content-Type': 'application/json'
        })
        return request

api='yljwWZQLpxsC5Pa0'
key='3To2MIyeguCllBPbR6YJifYAW7hW0GqI'
address = '3NRxCpzTNAitAxdueXT2d2D56Fn6EFkYBk'
client = Auth(api,key)
res_acc = requests.get(f"{URL}/v2/user",auth=client)
account_id =res_acc.json()["data"]["id"]
print(account_id)
data = {
    "type": "request",
    "to": "3AoNhmQAQKcaqsPp2YnGkK8RFpLHQ4owTt",
    "amount": "1",
    "currency": "BTC"
  }
response = requests.post(f"{URL}/v2/accounts/{account_id}/transactions",data=data,auth=client)

print(response.status_code)
print(response.json())