import json
from server.db.db_session import create_session
from server.db.models.__all_models import Group, User
import pytest


def test_get_user_groups_success(test_client, get_auth_token):
    """Тест на успешное получение групп пользователя."""
    token, user_id = get_auth_token
    db_sess = create_session()
    user = db_sess.get(User, user_id)
    group1 = Group(name="Group A")
    group2 = Group(name="Group B")
    user.groups.append(group1)
    user.groups.append(group2)
    db_sess.add(user)
    db_sess.commit()
    db_sess.close()

    response = test_client.get(
        "/groups/",
        data=json.dumps({"user_id": user_id}),
        content_type="application/json",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["user_id"] == user_id
    assert len(data["groups"]) == 2
    assert "Group A" in [g["name"] for g in data["groups"]]
    assert "Group B" in [g["name"] for g in data["groups"]]


def test_get_user_groups_no_user_id(test_client, get_auth_token):
    """Тест на получение групп без user_id."""
    token, _ = get_auth_token
    response = test_client.get(
        "/groups/",
        data=json.dumps({}),
        content_type="application/json",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400
    assert response.get_json()["error"] == "'user_id' is required"


def test_add_user_to_groups_success(test_client):
    """Тест на успешное добавление пользователя в группы."""
    db_sess = create_session()
    user = User(username="user_add", hashed_password="password")
    group1 = Group(name="Group 1")
    group2 = Group(name="Group 2")
    db_sess.add(user)
    db_sess.add(group1)
    db_sess.add(group2)
    db_sess.commit()
    user_id = user.id
    group_ids = [group1.id, group2.id]
    db_sess.close()

    response = test_client.post(
        "/groups/",
        data=json.dumps({"user_id": user_id, "group_ids": group_ids}),
        content_type="application/json"
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == f"User {user_id} added to groups"
    assert len(data["groups"]) == 2


def test_add_user_to_groups_invalid_group(test_client, get_auth_token):
    """Тест на попытку добавить пользователя в несуществующую группу."""
    token, user_id = get_auth_token
    response = test_client.post(
        "/groups/",
        data=json.dumps({"user_id": user_id, "group_ids": [999, 1000]}),
        content_type="application/json",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400
    assert response.get_json()["message"] == "No valid groups found"


def test_remove_user_from_groups_success(test_client, get_auth_token):
    """Тест на успешное удаление пользователя из групп."""
    token, user_id = get_auth_token
    db_sess = create_session()
    user = db_sess.get(User, user_id)
    group1 = Group(name="Group to Remove")
    group2 = Group(name="Group to Keep")
    user.groups.append(group1)
    user.groups.append(group2)
    db_sess.add(user)
    db_sess.add(group1)
    db_sess.add(group2)
    db_sess.commit()
    group_ids = [group1.id]
    db_sess.close()

    response = test_client.delete(
        f"/groups/",
        data=json.dumps({"group_ids": group_ids}),
        content_type="application/json",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == f"User {user_id} removed from specified groups"
    assert len(data["groups"]) == 1
    assert "Group to Keep" in [g["name"] for g in data["groups"]]

    db_sess = create_session()
    user = db_sess.get(User, user_id)
    assert len(user.groups) == 1
    db_sess.close()


def test_get_all_user_groups_success(test_client, get_auth_token):
    """Тест на получение всех групп пользователя через /all_user_groups."""
    token, user_id = get_auth_token
    db_sess = create_session()
    user = db_sess.get(User, user_id)
    group1 = Group(name="All Group 1")
    group2 = Group(name="All Group 2")
    user.groups.append(group1)
    user.groups.append(group2)
    db_sess.add(user)
    db_sess.commit()
    db_sess.close()

    response = test_client.get(
        f"/groups/all_user_groups",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["user_id"] == user_id
    assert len(data["groups"]) == 2
    assert "All Group 1" in [g["name"] for g in data["groups"]]
    assert "All Group 2" in [g["name"] for g in data["groups"]]
