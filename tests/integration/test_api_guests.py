from datetime import datetime
import json

import pytest

from app.domain.Guests import Guest, GuestDTO


def test_api_get_guests(client):
    response = client.get('/hospedes/')
    guests = json.loads(response.data)
    assert len(guests) == 4
    assert response.status_code == 200


def test_api_get_guests_id(client):
    response = client.get('/hospedes/00157624242')
    guests = json.loads(response.data)
    assert guests['name'] == 'Bento Luiz'
    assert response.status_code == 200


def test_api_get_guests_id_not_found(client):
    response = client.get('/hospedes/00157624')
    assert response.status_code == 404


def test_api_post_guests(client):
    guest_dto: GuestDTO = {
        'document':'03093331056',
        'name':'Ana Claudia',
        'surname':'Costa',
        'country':'Brazil',
        'phone':'4832395853',
        'created_at': None
        }

    response = client.post('/hospedes/cadastro', data=guest_dto)

    assert response.status_code == 201
    assert response.text == 'CREATED'


def test_api_post_guests_bad_request(client):
    response = client.post('/hospedes/cadastro', data=None)
    assert response.status_code == 400


def test_api_delete_guests(client):
    response = client.delete('/hospedes/00157624242')
    assert response.status_code == 200
    assert response.text == 'DELETED'


def test_api_delete_guests_not_found(client):
    response = client.delete('/hospedes/0015242')
    assert response.status_code == 404


def test_api_updated_guests(client):
    data: GuestDTO = {
        'document': "00157624242",
        'name': 'Bento Luiz',
        'surname': 'V M da S Neto',
        'country': 'Brazil',
        'phone': '48992054211',
        'created_at': None
    }
    response = client.put('/hospedes/', data=data)
    assert response.status_code == 200
    assert response.text == 'UPDATED'


def test_api_updated_guests_not_found(client):
    data: GuestDTO  = {
        'document': "0015724242",
        'name': 'Bento Luiz',
        'surname': 'V M da S Neto',
        'country': 'Brazil',
        'phone': '48992054211',
        'created_at': None
    }
    response = client.put('/hospedes/', data=data)
    assert response.status_code == 404



def test_api_updated_guests_bad_request(client):
    data = {
        'document': '',
        'name': 'Bento Luiz',
        'surname': 'V M da S Neto',
        'country': 'Brazil',
        'phone': '489920542115432'
    }
    response = client.put('/hospedes/', data=data)
    assert response.status_code == 400