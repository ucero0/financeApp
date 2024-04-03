from ..app.schemas.user import UserCreate
from .conftest import client,session
import pytest
from ..app.routes.user import userRoute

user_credentials = {"email": "test@gmail.com", "password": "password"}
aouthSchema = {"username": user_credentials["email"], "password": user_credentials["password"]}

@pytest.fixture
def createUser(client):
    response = client.post(userRoute.prefix,json=user_credentials,)
    print(response.json())
    assert response.status_code == 201
    newUser = response.json()
    return newUser
@pytest.fixture
def getToken(client):
    response = client.post("/token",data=aouthSchema,)
    token = response.json()
    return {"Authorization": f"Bearer {token['access_token']}"}

def test_connection_db(session):
    assert session is not None
def test_login(client,createUser):
    response = client.post("/token",data=aouthSchema,)
    assert response.status_code == 200

def test_login_invalid_user(client):
    response = client.post("/token",data=aouthSchema,)
    assert response.status_code == 401

def test_create_user(client):
    response = client.post(userRoute.prefix,json=user_credentials,)
    print(response.json())
    assert response.status_code == 201
    assert user_credentials["email"] == response.json()["email"]
    #2nd time should fail
    response = client.post(userRoute.prefix,json=user_credentials,)
    assert response.status_code == 400 and response.json() == {"detail": "Email already registered"}

def test_create_user_invalid_email(client):
    response = client.post(userRoute.prefix,
                           json={"email": "3453", "password": "password"}, )
    assert response.status_code == 422

def test_get_users(client, createUser):
    response = client.get(userRoute.prefix)
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_get_myUser(client,createUser,getToken):
    response = client.get(f"{userRoute.prefix}/me", headers=getToken)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_credentials["email"]

def test_delete_OwnUser(client,createUser,getToken):
    print(createUser)
    response = client.delete(f"{userRoute.prefix}/{createUser['email']}",headers=getToken) 
    assert response.status_code == 200
