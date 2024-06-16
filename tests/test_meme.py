import pytest
import pytest_asyncio
import io
from fastapi.testclient import TestClient
from tortoise import Tortoise
from public_api.setup import app
from public_api.database import get_config
from public_api.api import MemeDB, MemeCreate, MemeDelete

DATABASE_URL = 'sqlite://:memory:'


async def init_tortoise():
    await Tortoise.init(config=get_config(DATABASE_URL))
    await Tortoise.generate_schemas()


async def finalize_tortoise():
    await Tortoise.close_connections()


@pytest.mark.asyncio
@pytest_asyncio.fixture(scope='function')
async def setup_and_teardown_client():
    await init_tortoise()
    test_client = TestClient(app)
    yield test_client

    await finalize_tortoise()


def test_get_memes(setup_and_teardown_client):
    response = setup_and_teardown_client.get('/api/v1/memes/')
    assert response.status_code == 200
    assert type(response.json()) == list


def test_crud_meme(setup_and_teardown_client):
    # create
    with open(file='test.txt', mode='rb') as f:
        contents = f.read()
        byte_stream = io.BytesIO(contents)

    title = 'title'
    response = setup_and_teardown_client.post(f'/api/v1/memes/?title={title}', files={'file': byte_stream})
    assert response.status_code == 201
    assert MemeCreate.Response(**response.json())
    assert title == response.json()['meme']['title']

    # get
    meme_uuid = response.json()['meme']['uuid']
    response = setup_and_teardown_client.get(f'/api/v1/memes/{meme_uuid}')
    assert response.status_code == 200
    assert MemeDB(**response.json())

    response = setup_and_teardown_client.get('/api/v1/memes/123')
    assert response.status_code == 422

    # put
    title_new = 'title_new'
    response = setup_and_teardown_client.put(
        f'/api/v1/memes/{meme_uuid}?title={title_new}', files={'file': byte_stream}
    )
    assert response.status_code == 200
    assert MemeCreate.Response(**response.json())
    assert title_new == response.json()['meme']['title']

    # delete
    response = setup_and_teardown_client.delete(f'/api/v1/memes/{meme_uuid}')
    assert response.status_code == 200
    assert MemeDelete.Response(**response.json())

    response = setup_and_teardown_client.get(f'/api/v1/memes/{meme_uuid}')
    assert response.status_code == 404
