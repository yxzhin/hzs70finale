# test_user_group.py
import pytest
import os
import json
from server.app import create_app
from server.db.db_session import global_init, create_session
from server.db.models.__all_models import User, Group, UserGroup, Expense, ExpenseParticipant, Payment, Debt


@pytest.fixture(scope="session")
def test_client():
    db_path = "db/test.sqlite"
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = db_path
    with app.app_context():
        global_init(db_path)
    with app.test_client() as client:
        yield client
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
def setup_user_and_groups(db_session, get_auth_token):
    token, user_id = get_auth_token
    db_sess = db_session
    user = db_sess.get(User, user_id)
    group1 = Group(name="Group A", owner_id=user_id)
    group2 = Group(name="Group B", owner_id=user_id)
    db_sess.add_all([group1, group2])
    db_sess.commit()
    return token, user_id, [group1, group2]


# --- Тесты для GET /user_groups/ ---
def test_get_user_groups_success(test_client, setup_user_and_groups, db_session):
    token, user_id, groups = setup_user_and_groups
    user = db_session.get(User, user_id)
    user.groups.append(groups[0])
    db_session.commit()
    response = test_client.get(
        f"/user_groups/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["user_id"] == user_id
    assert len(data["groups"]) == 1
    assert "Group A" in [g["name"] for g in data["groups"]]


def test_get_user_groups_unauthorized(test_client):
    response = test_client.get("/user_groups/")
    assert response.status_code == 401
    assert response.get_json()["message"] == "Token is missing"


# --- Тесты для POST /user_groups/<group_id> ---
def test_add_user_to_group_success(test_client, setup_user_and_groups, db_session):
    token, user_id, groups = setup_user_and_groups
    group_to_add = groups[0]
    response = test_client.post(
        f"/user_groups/{group_to_add.id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == f"User {user_id} added to group {group_to_add.id}"
    assert len(data["groups"]) == 1
    user = db_session.get(User, user_id)
    assert len(user.groups) == 1
    assert group_to_add in user.groups


def test_add_user_to_group_already_in_group(test_client, setup_user_and_groups, db_session):
    token, user_id, groups = setup_user_and_groups
    group_to_add = groups[0]
    user = db_session.get(User, user_id)
    user.groups.append(group_to_add)
    db_session.commit()
    response = test_client.post(
        f"/user_groups/{group_to_add.id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == f"User {user_id} is already in group {group_to_add.id}"


def test_add_user_to_group_not_found(test_client, setup_user_and_groups):
    token, user_id, _ = setup_user_and_groups
    non_existent_group_id = 999
    response = test_client.post(
        f"/user_groups/{non_existent_group_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404
    assert response.get_json()["message"] == "Group not found"


# --- Тесты для DELETE /user_groups/<group_id> ---
def test_remove_user_from_group_success(test_client, setup_user_and_groups, db_session):
    token, user_id, groups = setup_user_and_groups
    user = db_session.get(User, user_id)
    group_to_remove = groups[0]
    user.groups.append(group_to_remove)
    db_session.commit()
    response = test_client.delete(
        f"/user_groups/{group_to_remove.id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == f"User {user_id} removed from group {group_to_remove.id}"
    assert len(data["groups"]) == 0
    db_session.refresh(user)
    assert len(user.groups) == 0


def test_remove_user_from_group_not_in_group(test_client, setup_user_and_groups):
    token, user_id, groups = setup_user_and_groups
    group_not_in = groups[0]
    response = test_client.delete(
        f"/user_groups/{group_not_in.id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == f"User {user_id} is not in group {group_not_in.id}"


def test_remove_user_from_non_existent_group(test_client, setup_user_and_groups):
    token, user_id, _ = setup_user_and_groups
    non_existent_group_id = 999
    response = test_client.delete(
        f"/user_groups/{non_existent_group_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404
    assert response.get_json()["message"] == "Group not found"
