import json
import pytest
from server.app import create_app
from server.db.db_session import global_init, create_session
from server.db.models.users import User


@pytest.fixture(scope="module")
def test_client():
    app = create_app()
    app.config["TESTING"] = True
    app.config[
        "SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/test.sqlite"  # Рекомендуется использовать абсолютный путь или memory

    with app.app_context():
        global_init("db/test.sqlite")

    with app.test_client() as client:
        yield client


@pytest.fixture(scope="function", autouse=True)
def clear_users():
    # Очистка таблицы пользователей перед каждым тестом
    session = create_session()
    session.query(User).delete()
    session.commit()
    session.close()
    yield


def test_register_user(test_client):
    response = test_client.post(
        "/user/register",
        data=json.dumps({
            "username": "testuser",
            "password": "secret"
        }),
        content_type="application/json"
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "User created and logged in"
    assert data["user"]["username"] == "testuser"


def test_register_duplicate_user(test_client):
    # Сначала создаём пользователя
    test_client.post(
        "/user/register",
        data=json.dumps({
            "username": "testuser",
            "password": "secret"
        }),
        content_type="application/json"
    )

    # Пытаемся создать того же пользователя ещё раз
    response = test_client.post(
        "/user/register",
        data=json.dumps({
            "username": "testuser",
            "password": "secret"
        }),
        content_type="application/json"
    )

    assert response.status_code == 400
    assert "User already exists" in response.get_json().get("error", "")


def test_login_user(test_client):
    # Регистрируем пользователя
    test_client.post(
        "/user/register",
        data=json.dumps({
            "username": "testuser",
            "password": "secret"
        }),
        content_type="application/json"
    )

    # Логинимся
    response = test_client.post(
        "/user/login",
        data=json.dumps({
            "username": "testuser",
            "password": "secret"
        }),
        content_type="application/json"
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "User logged in"
    assert "token" in data
    assert data["user"]["username"] == "testuser"


def test_login_wrong_password(test_client):
    # Регистрируем пользователя
    test_client.post(
        "/user/register",
        data=json.dumps({
            "username": "testuser",
            "password": "secret"
        }),
        content_type="application/json"
    )

    # Пытаемся войти с неправильным паролем
    response = test_client.post(
        "/user/login",
        data=json.dumps({
            "username": "testuser",
            "password": "wrongpassword"
        }),
        content_type="application/json"
    )

    assert response.status_code == 401
    assert response.get_json().get("error") == "Invalid username or password"


def test_get_current_user(test_client):
    # Регистрируем пользователя
    test_client.post(
        "/user/register",
        data=json.dumps({
            "username": "testuser",
            "password": "secret"
        }),
        content_type="application/json"
    )

    # Логинимся
    login_response = test_client.post(
        "/user/login",
        data=json.dumps({
            "username": "testuser",
            "password": "secret"
        }),
        content_type="application/json"
    )
    token = login_response.get_json().get("token")

    # Запрашиваем текущего пользователя с токеном
    response = test_client.get(
        "/user/current_user",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["username"] == "testuser"
