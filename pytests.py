import pytest
import requests
import json
from data import employees

@pytest.fixture
def token():
    url = 'http://127.0.0.1:8000/login'
    data = {'username': 'alice', 'password': 'alice123'}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return response.json().get('token')


def test_successful_login():
    url = 'http://127.0.0.1:8000/login'
    data = {'username': 'alice', 'password': 'alice123'}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    assert 'token' in response.json()


def test_successful_salary_request(token):
    url = 'http://127.0.0.1:8000/salary'
    headers = {'Authorization': 'Bearer ' + token}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    assert 'salary' in response.json()


def test_failed_salary_request_no_token():
    url = 'http://127.0.0.1:8000/salary'
    response = requests.get(url)
    assert response.status_code == 200
    assert 'error' in response.json()
