import os

import pytest

from drf_yasg.codecs import yaml_sane_load


@pytest.mark.urls('urlconfs.drf_openapi_urls')
def test_versioned_v1(client):
    response = client.get('/v1.0/swagger.yaml')
    assert response.status_code == 200
    swagger = yaml_sane_load(response.content.decode('utf-8'))
    assert '/v1.0/snippets/' in swagger['paths']
    versioned_get = swagger['paths']['/v1.0/snippets/']['get']
    assert 'title' not in versioned_get['responses']['200']['schema']['required']
    assert 'v1field' in versioned_get['responses']['200']['schema']['properties']
    assert 'v2field' not in versioned_get['responses']['200']['schema']['properties']


@pytest.mark.urls('urlconfs.drf_openapi_urls')
def test_versioned_v2(client):
    response = client.get('/v2.0/swagger.yaml')
    assert response.status_code == 200
    swagger = yaml_sane_load(response.content.decode('utf-8'))
    assert '/v2.0/snippets/' in swagger['paths']
    versioned_get = swagger['paths']['/v2.0/snippets/']['get']
    assert 'title' in versioned_get['responses']['200']['schema']['required']
    assert 'v1field' in versioned_get['responses']['200']['schema']['properties']
    assert 'v2field' in versioned_get['responses']['200']['schema']['properties']


@pytest.mark.urls('urlconfs.drf_openapi_urls')
def test_reference_schema(client, compare_schemas):
    response = client.get('/v2.0/swagger.yaml')
    assert response.status_code == 200
    swagger = yaml_sane_load(response.content.decode('utf-8'))

    with open(os.path.join(os.path.dirname(__file__), 'reference_drf_openapi.yaml')) as reference:
        reference_schema = yaml_sane_load(reference)

    compare_schemas(swagger, reference_schema)


@pytest.mark.urls('urlconfs.drf_openapi_urls')
def test_response_validation(client):
    response = client.get('/v2.0/snippets/')
    assert response.status_code == 400
