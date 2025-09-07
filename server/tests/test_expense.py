# -*- coding: utf-8 -*-
import json
from datetime import datetime

import pytest

from server.db import db_session
# Правильный импорт из файла conftest
from server.tests.conftest import create_group_and_get_id


def test_create_expense_success(test_client, get_auth_token, db_session):
    """
    Тест успешного создания расхода.
    """
    token, user_id = get_auth_token
    # Передаём правильные фикстуры: db_session и user_id
    group_id = create_group_and_get_id(db_session, user_id)

    payload = {
        "group_id": group_id,
        "title": "Dinner",
        "amount": 100.0,
        "currency": "USD",
        "expense_type": "shared",
        "split_type": "equal",
        "payment_method": "cash",
        "next_payment_date": datetime.now().isoformat(),
        "is_paid": True,
        "participants": [
            {"user_id": user_id, "amount": 100.0}
        ],
        "payments": [
            {"payer_id": user_id, "amount": 100.0}
        ]
    }

    response = test_client.post(
        # Исправлено: используем правильный URL для создания расхода
        "/expense/",
        data=json.dumps(payload),
        headers={"Authorization": f"Bearer {token}"},
        content_type="application/json"
    )
    # 💡 Добавлено: Вывод сообщения при ошибке
    assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}. Response: {response.get_data(as_text=True)}"
    data = response.get_json()
    assert "expense_id" in data
    assert data["message"] == "Expense added successfully"




def test_create_expense_missing_field(test_client, get_auth_token, db_session):
    """
    Тест создания расхода с пропущенным полем.
    """
    token, user_id = get_auth_token
    group_id = create_group_and_get_id(db_session, user_id)

    # Убираем поле 'amount'
    payload = {
        "group_id": group_id,
        "title": "Dinner",
        "currency": "USD",
        "expense_type": "shared",
        "split_type": "equal",
        "payment_method": "cash",
        "next_payment_date": datetime.now().isoformat(),
        "is_paid": False,
        "participants": [
            {"user_id": user_id, "amount": 50.0}
        ]
    }

    response = test_client.post(
        # Исправлено: используем правильный URL для создания расхода
        "/expense/",
        data=json.dumps(payload),
        headers={"Authorization": f"Bearer {token}"},
        content_type="application/json"
    )
    # 💡 Добавлено: Вывод сообщения при ошибке
    assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}. Response: {response.get_data(as_text=True)}"
    assert "amount is required" in response.get_json()["message"]




def test_get_expense_by_id(test_client, get_auth_token, db_session):
    """
    Тест получения расхода по ID.
    """
    token, user_id = get_auth_token
    group_id = create_group_and_get_id(db_session, user_id)

    # Создаём расход
    payload = {
        "group_id": group_id,
        "title": "Pizza",
        "amount": 50.0,
        "currency": "USD",
        "expense_type": "shared",
        "split_type": "equal",
        "payment_method": "cash",
        "next_payment_date": datetime.now().isoformat(),
        "is_paid": True,
        "participants": [
            {"user_id": user_id, "amount": 50.0}
        ],
        "payments": [
            {"payer_id": user_id, "amount": 50.0}
        ]
    }

    post_resp = test_client.post(
        # Исправлено: используем правильный URL для создания расхода
        "/expense/",
        data=json.dumps(payload),
        headers={"Authorization": f"Bearer {token}"},
        content_type="application/json"
    )

    expense_id = post_resp.get_json()["expense_id"]

    # Получаем его
    response = test_client.get(f"/expense/{expense_id}")
    # 💡 Добавлено: Вывод сообщения при ошибке
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}. Response: {response.get_data(as_text=True)}"
    data = response.get_json()
    assert data["title"] == "Pizza"
    assert data["amount"] == 50.0




def test_get_nonexistent_expense(test_client):
    """
    Тест получения несуществующего расхода.
    """
    response = test_client.get("/expense/99999")
    # 💡 Добавлено: Вывод сообщения при ошибке
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}. Response: {response.get_data(as_text=True)}"
    assert response.get_json()["message"] == "Expense not found"




def test_get_all_expenses_of_group(test_client, get_auth_token, db_session):
    """
    Тест получения всех расходов группы.
    """
    token, user_id = get_auth_token
    group_id = create_group_and_get_id(db_session, user_id)

    # Создаём один расход
    payload = {
        "group_id": group_id,
        "title": "Groceries",
        "amount": 30.0,
        "currency": "USD",
        "expense_type": "shared",
        "split_type": "equal",
        "payment_method": "cash",
        "next_payment_date": datetime.now().isoformat(),
        "is_paid": True,
        "participants": [
            {"user_id": user_id, "amount": 30.0}
        ],
        "payments": [
            {"payer_id": user_id, "amount": 30.0}
        ]
    }

    test_client.post(
        # Исправлено: используем правильный URL для создания расхода
        "/expense/",
        data=json.dumps(payload),
        headers={"Authorization": f"Bearer {token}"},
        content_type="application/json"
    )

    # Получаем список всех расходов группы
    response = test_client.get(f"/expense/group/{group_id}")
    # 💡 Добавлено: Вывод сообщения при ошибке
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}. Response: {response.get_data(as_text=True)}"
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["title"] == "Groceries"




def test_get_group_expenses_empty(test_client, get_auth_token, db_session):
    """
    Тест получения расходов пустой группы.
    """
    token, user_id = get_auth_token
    group_id = create_group_and_get_id(db_session, user_id)

    response = test_client.get(f"/expense/group/{group_id}")
    # 💡 Добавлено: Вывод сообщения при ошибке
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}. Response: {response.get_data(as_text=True)}"
    assert response.get_json()["message"] == "No expenses found"




def test_expense_history_pagination(test_client, get_auth_token, db_session):
    """
    Тест пагинации истории расходов.
    """
    token, user_id = get_auth_token
    group_id = create_group_and_get_id(db_session, user_id)

    # Добавим 5 расходов
    for i in range(5):
        payload = {
            "group_id": group_id,
            "title": f"Item {i}",
            "amount": 20.0,
            "currency": "USD",
            "expense_type": "shared",
            "split_type": "equal",
            "payment_method": "cash",
            "next_payment_date": datetime.now().isoformat(),
            "is_paid": True,
            "participants": [
                {"user_id": user_id, "amount": 20.0}
            ],
            "payments": [
                {"payer_id": user_id, "amount": 20.0}
            ]
        }

        test_client.post(
            # Исправлено: используем правильный URL для создания расхода
            "/expense/",
            data=json.dumps(payload),
            headers={"Authorization": f"Bearer {token}"},
            content_type="application/json"
        )

    # Получаем первую страницу
    response = test_client.post(
        "/expense/history",
        data=json.dumps({
            "group_id": group_id,
            "page": 1,
            "items_per_page": 2
        }),
        headers={"Authorization": f"Bearer {token}"},
        content_type="application/json"
    )

    # 💡 Добавлено: Вывод сообщения при ошибке
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}. Response: {response.get_data(as_text=True)}"
    data = response.get_json()
    assert data["page"] == 1
    assert data["items_per_page"] == 2
    assert data["total_pages"] >= 3
    assert len(data["expenses"]) == 2