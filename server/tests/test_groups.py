import pytest
import json
from server.db.models.__all_models import Group, User, UserGroup


# Фикстура для создания тестовых пользователей
@pytest.fixture
def create_test_users(db_session):
    user1 = User(username="test_user1", hashed_password="hashed_password")
    user2 = User(username="test_user2", hashed_password="hashed_password")
    db_session.add_all([user1, user2])
    db_session.commit()
    return user1, user2


# Фикстура для создания тестовой группы
@pytest.fixture
def create_test_group(db_session, get_auth_token):
    _, owner_id = get_auth_token
    user1 = User(username="group_user_1", hashed_password="hashed_password")
    user2 = User(username="group_user_2", hashed_password="hashed_password")
    db_session.add_all([user1, user2])
    db_session.commit()

    group = Group(name="TestGroup", owner_id=owner_id)
    db_session.add(group)
    db_session.flush()

    user_group1 = UserGroup(user_id=owner_id, group_id=group.id)
    user_group2 = UserGroup(user_id=user1.id, group_id=group.id)
    user_group3 = UserGroup(user_id=user2.id, group_id=group.id)
    db_session.add_all([user_group1, user_group2, user_group3])
    db_session.commit()
    return group, [owner_id, user1.id, user2.id]


def test_get_group_success(test_client, create_test_group):
    group, user_ids = create_test_group
    response = test_client.get(f"/groups/{group.id}")

    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == group.id
    assert data["name"] == "TestGroup"
    assert len(data["users"]) == len(user_ids)

    returned_user_ids = {user["id"] for user in data["users"]}
    assert returned_user_ids == set(user_ids)


def test_get_group_not_found(test_client):
    response = test_client.get("/groups/999")
    assert response.status_code == 404
    assert response.get_json()["message"] == "group not found"


def test_create_group_success(test_client, db_session, get_auth_token, create_test_users):
    token, owner_id = get_auth_token
    user1, user2 = create_test_users
    user_ids = [owner_id, user1.id, user2.id]

    response = test_client.post(
        "/groups/",
        data=json.dumps({"name": "New Awesome Group", "users": user_ids}),
        content_type="application/json",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "group created"
    assert data["group"]["name"] == "New Awesome Group"
    assert db_session.query(Group).filter_by(name="New Awesome Group").count() == 1


def test_create_group_missing_fields(test_client, get_auth_token):
    token, _ = get_auth_token
    response = test_client.post(
        "/groups/",
        data=json.dumps({"name": "New Awesome Group"}),
        content_type="application/json",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400
    assert response.get_json()["message"] == "group name and users are required"


def test_create_group_name_exists(test_client, db_session, get_auth_token):
    token, owner_id = get_auth_token
    existing_group = Group(name="Existing Group", owner_id=owner_id)
    db_session.add(existing_group)
    db_session.commit()
    response = test_client.post(
        "/groups/",
        data=json.dumps({"name": "Existing Group", "users": [owner_id]}),
        content_type="application/json",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403
    assert response.get_json()["message"] == "group already exists"


def test_create_group_user_not_found(test_client, get_auth_token):
    token, owner_id = get_auth_token
    response = test_client.post(
        "/groups/",
        data=json.dumps({"name": "New Group", "users": [owner_id, 999]}),
        content_type="application/json",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404
    assert response.get_json()["message"] == "a user with an id of 999 not found"


def test_create_group_duplicate_user(test_client, get_auth_token):
    token, owner_id = get_auth_token
    response = test_client.post(
        "/groups/",
        data=json.dumps({"name": "New Group", "users": [owner_id, owner_id]}),
        content_type="application/json",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400
    assert response.get_json()["message"] == f"user with id {owner_id} is duplicated"


def test_create_group_unauthorized(test_client):
    response = test_client.post(
        "/groups/",
        data=json.dumps({"name": "New Group", "users": [1]}),
        content_type="application/json"
    )
    assert response.status_code == 401
    assert response.get_json()["message"] == "Token is missing"


def test_update_group_success(test_client, db_session, get_auth_token):
    token, owner_id = get_auth_token
    group = Group(name="Old Name", owner_id=owner_id)
    db_session.add(group)
    db_session.commit()
    response = test_client.put(
        f"/groups/{group.id}",
        data=json.dumps({"name": "New Name"}),
        content_type="application/json",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.get_json()["message"] == "group updated"
    updated_group = db_session.query(Group).get(group.id)
    assert updated_group.name == "New Name"


def test_update_group_not_found(test_client, get_auth_token):
    token, _ = get_auth_token
    response = test_client.put(
        "/groups/999",
        data=json.dumps({"name": "New Name"}),
        content_type="application/json",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404
    assert response.get_json()["message"] == "group not found"


def test_update_group_permission_denied(test_client, db_session, get_auth_token):
    token, _ = get_auth_token
    other_user = User(username="other_user", hashed_password="hashed_password")
    db_session.add(other_user)
    db_session.commit()
    group = Group(name="Other User's Group", owner_id=other_user.id)
    db_session.add(group)
    db_session.commit()
    response = test_client.put(
        f"/groups/{group.id}",
        data=json.dumps({"name": "New Name"}),
        content_type="application/json",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403
    assert response.get_json()["message"] == "permission denied"


def test_delete_group_success(test_client, db_session, get_auth_token):
    token, owner_id = get_auth_token
    group = Group(name="Group to Delete", owner_id=owner_id)
    db_session.add(group)
    db_session.flush()  # Или db_session.commit(), чтобы получить group.id
    user_group = UserGroup(user_id=owner_id, group_id=group.id)
    db_session.add(user_group)
    db_session.commit()
    group_id = group.id
    response = test_client.delete(
        f"/groups/{group_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.get_json()["message"] == "group deleted"
    assert db_session.query(Group).get(group_id) is None
    assert db_session.query(UserGroup).filter_by(group_id=group_id).count() == 0


def test_delete_group_not_found(test_client, get_auth_token):
    token, _ = get_auth_token
    response = test_client.delete(
        "/groups/999",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404
    assert response.get_json()["message"] == "group not found"


def test_delete_group_permission_denied(test_client, db_session, get_auth_token):
    token, _ = get_auth_token
    other_user = User(username="other_user", hashed_password="hashed_password")
    db_session.add(other_user)
    db_session.commit()
    group = Group(name="Other Group", owner_id=other_user.id)
    db_session.add(group)
    db_session.commit()
    response = test_client.delete(
        f"/groups/{group.id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403
    assert response.get_json()["message"] == "permission denied"


def test_get_all_user_groups_success(test_client, db_session, get_auth_token):
    token, user_id = get_auth_token
    group1 = Group(name="Group 1", owner_id=user_id)
    group2 = Group(name="Group 2", owner_id=user_id)
    db_session.add_all([group1, group2])
    db_session.flush()
    user_group1 = UserGroup(user_id=user_id, group_id=group1.id)
    user_group2 = UserGroup(user_id=user_id, group_id=group2.id)
    db_session.add_all([user_group1, user_group2])
    db_session.commit()
    response = test_client.get(
        "/groups/all_user_groups",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["user_id"] == user_id
    assert len(data["groups"]) == 2
    group_names = {group["name"] for group in data["groups"]}
    assert "Group 1" in group_names
    assert "Group 2" in group_names


def test_get_all_user_groups_user_not_found(test_client, get_auth_token, db_session):
    token, user_id = get_auth_token
    db_session.query(User).filter_by(id=user_id).delete()
    db_session.commit()
    response = test_client.get(
        "/groups/all_user_groups",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404
    assert response.get_json()["message"] == "User not found"


def test_get_all_user_groups_unauthorized(test_client):
    response = test_client.get("/groups/all_user_groups")
    assert response.status_code == 401
    assert response.get_json()["message"] == "Token is missing"
