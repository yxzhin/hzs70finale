# -*- coding: utf-8 -*-
import pytest
import os
import json
from server.app import create_app
from server.db.db_session import global_init, create_session
from server.db.models.__all_models import User, Group, UserGroup, Expense, ExpenseParticipant, Payment, Debt


@pytest.fixture(scope="session")
def test_client():
    # Задаем путь к тестовой базе данных
    db_path = "db/test.sqlite"
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = db_path

    # Инициализация базы данных
    with app.app_context():
        global_init(db_path)

    # Предоставление тестового клиента
    with app.test_client() as client:
        yield client

    # Код после 'yield' выполняется после завершения всех тестов
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"\nDeleted test database file: {db_path}")


@pytest.fixture(scope="function")
def db_session():
    session = create_session()
    yield session
    session.rollback()
    session.close()


@pytest.fixture(autouse=True)
def clean_tables(db_session):
    # Очистка таблиц перед каждым тестом
    db_session.query(User).delete()
    db_session.query(Group).delete()
    db_session.query(UserGroup).delete()
    db_session.query(Expense).delete()
    db_session.query(ExpenseParticipant).delete()
    db_session.query(Payment).delete()
    db_session.query(Debt).delete()

    db_session.commit()


@pytest.fixture
def get_auth_token(test_client, clean_tables):
    # Регистрируем пользователя
    test_client.post(
        "/user/register",
        data=json.dumps({"username": "testuser", "password": "secret"}),
        content_type="application/json"
    )

    # Логинимся и получаем токен
    login_response = test_client.post(
        "/user/login",
        data=json.dumps({"username": "testuser", "password": "secret"}),
        content_type="application/json"
    )
    data = login_response.get_json()
    token = data.get("token")
    user_id = data["user"]["id"]

    return token, user_id


def create_group_and_get_id(db_session, user_id):
    """
    Создаёт новую группу в базе данных и возвращает её ID.

    :param db_session: Фикстура сессии базы данных pytest.
    :param user_id: ID пользователя, который будет добавлен в группу.
    :return: ID созданной группы.
    """
    # Исправление: Сначала находим объект пользователя по его ID
    user = db_session.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError(f"User with ID {user_id} not found.")

    # Создаём новую группу, добавляя найденный объект пользователя
    # Обязательно указываем владельца группы (owner)
    group = Group(name="test group", users=[user], owner=user)
    db_session.add(group)
    db_session.commit()
    return group.id
