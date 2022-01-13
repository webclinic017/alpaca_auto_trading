import requests
import os


srv_host, srv_port = os.getenv('DJANGO_SERVER_HOST'), os.getenv('DJANGO_SERVER_PORT')
if not srv_host:
    host = 'localhost:8000'
elif srv_port:
    host = f'{srv_host}:{srv_port}'
else:
    host = srv_host


def test_connection():    
    token_res = requests.post(f'http://{host}/api/token/')
    assert token_res.text == '{"username":["This field is required."],"password":["This field is required."]}'

def test_token_retrieval_failure():
    token_res = requests.post(f'http://{host}/api/token/', data={'username':'user1', 'password':'1'})
    assert token_res.text == '{"detail":"No active account found with the given credentials"}'

def test_token_retrieval_success():
    token_res = requests.post(f'http://{host}/api/token/', data={'username':'user1', 'password':'C@3vsRdNts8R5#N'})
    assert 'access' in token_res.json()

def test_token_refresh_failure():
    refresh_res = requests.post(f'http://{host}/api/token/refresh/', data={'refresh':'1'})
    assert refresh_res.text == '{"detail":"Token is invalid or expired","code":"token_not_valid"}'

def test_token_refresh_success():
    token_res = requests.post(f'http://{host}/api/token/', data={'username':'user1', 'password':'C@3vsRdNts8R5#N'})
    refresh = token_res.json()['refresh']
    refresh_res = requests.post(f'http://{host}/api/token/refresh/', data={'refresh':refresh})
    assert 'access' in refresh_res.json()

def test_sample_api_invalid_token():
    res = requests.get(f'http://{host}/api/sample/', headers={'Authorization': f'Bearer 1'})
    assert res.text == '{"detail":"Given token not valid for any token type","code":"token_not_valid","messages":[{"token_class":"AccessToken","token_type":"access","message":"Token is invalid or expired"}]}'
    
def test_sample_api_no_token():
    res = requests.get(f'http://{host}/api/sample/')
    assert res.text == '{"detail":"Authentication credentials were not provided."}'

def test_sample_api_successful_hit():
    token_res = requests.post(f'http://{host}/api/token/', data={'username':'user1', 'password':'C@3vsRdNts8R5#N'})
    access_token = token_res.json()['access']
    res = requests.get(f'http://{host}/api/sample/', headers={'Authorization': f'Bearer {access_token}'})
    assert res.text == '[{"a":"SampleAPI1"}]'

def test_permission_denied():
    token_res = requests.post(f'http://{host}/api/token/', data={'username':'user1', 'password':'C@3vsRdNts8R5#N'})
    access_token = token_res.json()['access']
    res = requests.get(f'http://{host}/api/users/', headers={'Authorization': f'Bearer {access_token}'})
    assert res.text == '{"detail":"You do not have permission to perform this action."}'
    