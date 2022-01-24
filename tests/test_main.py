# mypy: no-disallow-untyped-decorators
# pylint: disable=E0611,E0401
from typing import Generator
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from main import app_test, JWT_SECRET
from characters import Character, CharacterIn_Pydantic
from tortoise.contrib.test import finalizer, initializer
from tortoise.contrib.fastapi import register_tortoise
import jwt

register_tortoise(
    app_test,
    db_url="postgres://postgres:postgres@localhost:5432/wod_npc_test",
    modules={'models': ['main']},
    generate_schemas= True,
    add_exception_handlers=True
)

@pytest.fixture(scope="function")
def client() -> Generator:
    initializer(modules=["main"], db_url="postgres://postgres:postgres@localhost:5432/wod_npc_test")
    with TestClient(app_test) as c:
        yield c
    finalizer()

def test_create_user(client: TestClient):  # nosec
    response = client.post("/api/users", json={"username": "Roko", "password_hash" : "lagartito5"})
    assert response.status_code == status.HTTP_201_CREATED, response.text
    data = response.json()
    assert data["username"] == "Roko"
    assert "id" in data

def test_create_user_duplicate(client: TestClient):  # nosec
    client.post("/api/users", json={"username": "Roko", "password_hash" : "lagartito5"})
    response2 = client.post("/api/users", json={"username": "Roko", "password_hash" : "lagartito5"})
    assert response2.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response2.text

def test_login(client: TestClient):
    client.post("/api/users", json={"username": "Roko", "password_hash" : "lagartito5"})
    response = client.post("/api/login", data={"username": "Roko", "password": "lagartito5"})
    assert jwt.decode(response.json()["access_token"], JWT_SECRET, algorithms=['HS256']).get("username") == "Roko"

def test_login_wrong(client: TestClient):
    client.post("/api/users", json={"username": "Roko", "password_hash" : "lagartito5"})
    response = client.post("/api/login", data={"username": "Roko", "password": "wrong_pass"})
    assert response.json()["detail"] == "Invalid username or password"

def test_get_myself(client: TestClient):
    client.post("/api/users", json={"username": "Roko", "password_hash" : "lagartito5"})
    jwt_response = client.post("/api/login", data={"username": "Roko", "password": "lagartito5"}).json()
    assert client.get("/api/users/me", headers={"Authorization" : "Bearer " + jwt_response["access_token"]}).json()["username"] == 'Roko'

def test_get_myself_unauthorized(client: TestClient):
    assert client.get("/api/users/me").json()["detail"] == 'Not authenticated'

@pytest.mark.asyncio
async def test_create_character(client:TestClient):
    client.post("/api/users", json={"username": "Roko", "password_hash" : "lagartito5"})
    jwt_response = client.post("/api/login", data={"username": "Roko", "password": "lagartito5"}).json()
    c = await CharacterIn_Pydantic.from_tortoise_orm(Character(id=1))

    assert len(client.post("/api/characters", json=c.__dict__, headers={"Authorization" : "Bearer " + jwt_response["access_token"]}).json().keys()) == 67

@pytest.mark.asyncio
async def test_get_characters(client:TestClient):
    client.post("/api/users", json={"username": "Roko", "password_hash" : "lagartito5"})
    jwt_response_r = client.post("/api/login", data={"username": "Roko", "password": "lagartito5"}).json()

    c1 = await CharacterIn_Pydantic.from_tortoise_orm(Character(id=1))
    c2 = await CharacterIn_Pydantic.from_tortoise_orm(Character(id=1))
    c3 = await CharacterIn_Pydantic.from_tortoise_orm(Character(id=1))

    b1 = await CharacterIn_Pydantic.from_tortoise_orm(Character(id=1, user_id=2))
    b2 = await CharacterIn_Pydantic.from_tortoise_orm(Character(id=1, user_id=2))

    client.post("/api/characters", json=c1.__dict__, headers={"Authorization" : "Bearer " + jwt_response_r["access_token"]})
    client.post("/api/characters", json=c2.__dict__, headers={"Authorization" : "Bearer " + jwt_response_r["access_token"]})
    client.post("/api/characters", json=c3.__dict__, headers={"Authorization" : "Bearer " + jwt_response_r["access_token"]})

    client.post("/api/users", json={"username": "Sicro", "password_hash" : "playa"})
    jwt_response_s = client.post("/api/login", data={"username": "Sicro", "password": "playa"}).json()

    client.post("/api/characters", json=b1.__dict__, headers={"Authorization" : "Bearer " + jwt_response_s["access_token"]})
    client.post("/api/characters", json=b2.__dict__, headers={"Authorization" : "Bearer " + jwt_response_s["access_token"]})

    assert len(client.get("/api/characters", headers={"Authorization" : "Bearer " + jwt_response_r["access_token"]}).json())== 3
    assert len(client.get("/api/characters", headers={"Authorization" : "Bearer " + jwt_response_s["access_token"]}).json()) == 2

@pytest.mark.asyncio
async def test_get_characters_not_logged(client:TestClient):
    client.post("/api/users", json={"username": "Roko", "password_hash" : "lagartito5"})
    jwt_response_r = client.post("/api/login", data={"username": "Roko", "password": "lagartito5"}).json()

    c1 = await CharacterIn_Pydantic.from_tortoise_orm(Character(id=1))

    client.post("/api/characters", json=c1.__dict__, headers={"Authorization" : "Bearer " + jwt_response_r["access_token"]})

    assert client.get("/api/characters").json()["detail"] == "Not authenticated"

    # Documentation: ["https://tortoise-orm.readthedocs.io/en/latest/examples/fastapi.html#tests-py", ]
