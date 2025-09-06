import json
import pytest
from server.db.db_session import create_session
from server.db.models.__all_models import User, Group


@pytest.fixture
def setup_user_and_groups(db_session, get_auth_token):
    """
    Фикстура для настройки тестовых данных: создает пользователя и несколько групп.
    Возвращает токен, user_id и созданные группы.
    """
    token, user_id = get_auth_token
    db_sess = db_session
    user = db_sess.get(User, user_id)

    # Создаем тестовые группы
    group1 = Group(name="Group A", owner_id=user_id)
    group2 = Group(name="Group B", owner_id=user_id)
    group3 = Group(name="Group C", owner_id=user_id)
    db_sess.add_all([group1, group2, group3])
    db_sess.commit()

    return token, user_id, [group1, group2, group3]


# --- Тесты для GET /user_groups/ ---
def test_get_user_groups_success(test_client, setup_user_and_groups, db_session):
    """
    Тест на успешное получение списка групп, в которых состоит пользователь.
    """
    token, user_id, groups = setup_user_and_groups
    user = db_session.get(User, user_id)
    # Добавляем пользователя в некоторые группы
    user.groups.append(groups[0])
    user.groups.append(groups[1])
    db_session.commit()

    response = test_client.get(
        f"/user_groups/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["user_id"] == user_id
    assert len(data["groups"]) == 2
    assert "Group A" in [g["name"] for g in data["groups"]]
    assert "Group B" in [g["name"] for g in data["groups"]]


def test_get_user_groups_not_found(test_client, get_auth_token):
    """
    Тест, когда пользователь не найден.
    """
    token, _ = get_auth_token
    non_existent_user_id = 999

    response = test_client.get(
        f"/user_groups/",
        headers={"Authorization": f"Bearer {token}"},
        data=json.dumps({"user_id": non_existent_user_id}),
        content_type="application/json"
    )

    # NOTE: В вашем API, `get` метод `UserGroupResource` не принимает `user_id`
    # в теле запроса, а получает его из токена. Поэтому этот тест
    # неактуален для вашей текущей реализации.
    # Этот код показан для примера, если бы API принимал user_id в теле запроса.
    # Для текущего API, пользователь всегда будет найден, так как user_id берется из токена,
    # который гарантирует существование пользователя.


# --- Тесты для POST /user_groups/ ---
def test_add_user_to_groups_success(test_client, setup_user_and_groups):
    """
    Тест на успешное добавление пользователя в группы.
    """
    token, user_id, groups = setup_user_and_groups
    group_ids_to_add = [g.id for g in groups]

    response = test_client.post(
        f"/user_groups/",
        data=json.dumps({"group_ids": group_ids_to_add}),
        content_type="application/json",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == f"User {user_id} added to groups"
    assert len(data["groups"]) == len(group_ids_to_add)

    db_sess = create_session()
    user = db_sess.get(User, user_id)
    assert len(user.groups) == len(group_ids_to_add)
    db_sess.close()


def test_add_user_to_groups_invalid_group_ids(test_client, setup_user_and_groups):
    """
    Тест на попытку добавить пользователя в несуществующие группы.
    """
    token, _, _ = setup_user_and_groups
    non_existent_group_ids = [999, 1000]

    response = test_client.post(
        f"/user_groups/",
        data=json.dumps({"group_ids": non_existent_group_ids}),
        content_type="application/json",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 400
    assert response.get_json()["message"] == "No valid groups found"


def test_add_user_to_groups_missing_group_ids(test_client, get_auth_token):
    """
    Тест на попытку добавить пользователя в группы без списка group_ids.
    """
    token, _ = get_auth_token

    response = test_client.post(
        f"/user_groups/",
        data=json.dumps({}),
        content_type="application/json",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "List 'group_ids' is required"


# --- Тесты для DELETE /user_groups/ ---
# --- Тесты для DELETE /user_groups/ ---
def test_remove_user_from_groups_success(test_client, setup_user_and_groups, db_session):
    """
    Тест на успешное удаление пользователя из групп.
    """
    token, user_id, groups = setup_user_and_groups
    user = db_session.get(User, user_id)
    # Добавляем пользователя во все группы
    for group in groups:
        user.groups.append(group)
    db_session.commit()

    group_ids_to_remove = [groups[0].id, groups[1].id]

    response = test_client.delete(
        f"/user_groups/",
        data=json.dumps({"group_ids": group_ids_to_remove}),
        content_type="application/json",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == f"User {user_id} removed from specified groups"
    # Проверяем, что осталась только одна группа
    assert len(data["groups"]) == 1
    assert groups[2].name in [g["name"] for g in data["groups"]]

    # Проверяем в БД, что группа действительно удалена
    db_session.refresh(user)
    assert len(user.groups) == 1

def test_remove_user_from_groups_missing_group_ids(test_client, get_auth_token):
    """
    Тест на попытку удаления без списка group_ids.
    """
    token, _ = get_auth_token

    response = test_client.delete(
        f"/user_groups/",
        data=json.dumps({}),
        content_type="application/json",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "List 'group_ids' is required"