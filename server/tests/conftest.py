import pytest
import json
from server.app import create_app
from server.db.db_session import global_init, create_session
from server.db.models.__all_models import User, Group, UserGroup, Expense, ExpenseParticipant, Payment, Debt


@pytest.fixture(scope="session")
def test_client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "db/test.sqlite"

    with app.app_context():
        global_init("db/test.sqlite")

    with app.test_client() as client:
        yield client


@pytest.fixture(scope="function")
def db_session():
    session = create_session()
    yield session
    session.rollback()
    session.close()


@pytest.fixture(autouse=True)
def clean_tables(db_session):
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

    login_response = test_client.post(
        "/user/login",
        data=json.dumps({"username": "testuser", "password": "secret"}),
        content_type="application/json"
    )
    data = login_response.get_json()
    token = data.get("token")
    user_id = data["user"]["id"]

    return token, user_id


@pytest.fixture
def create_category():
    session = create_session()

    category = ListingCategory(name="Test Category")
    session.add(category)
    session.commit()

    yield category
    session.delete(category)
    session.commit()

    session.close()
