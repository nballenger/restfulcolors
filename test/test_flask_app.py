import json

import pytest

from restfulcolors import app


@pytest.fixture
def client():
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


def test_get_color(client):
    response = client.get('/api/v1/colors/ff00ff')
    json_data = json.loads(response.data.decode('utf8'))

    top_level_keys = ['attributes', 'links', 'colorcode', 'href']
    for k in top_level_keys:
        assert k in list(json_data.keys())

    assert type(json_data['attributes']) == dict
    assert type(json_data['links']) == dict
    assert json_data['colorcode'] == 'ff00ff'
    assert json_data['href'] == '/api/v1/colors/ff00ff'
