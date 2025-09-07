from flask import Blueprint, jsonify
from datetime import datetime, timedelta, timezone
from server.db.db_session import create_session
from server.db.models.__all_models import (
    User,
    ExpenseCategory,
    Group,
    Expense,
    ExpenseParticipant,
    Payment,
    Debt,
)

test_bp = Blueprint("test", __name__)


@test_bp.route("/add_db_test_data", methods=["GET"])
def test_data():
    db_session = create_session()
    # === USERS ===
    user1 = User(username="seva", hashed_password="")
    user2 = User(username="lesha", hashed_password="")
    user3 = User(username="filip", hashed_password="")
    user4 = User(username="grisha", hashed_password="")
    user1.set_password("password")
    user2.set_password("password")
    user3.set_password("password")
    user4.set_password("password")

    db_session.add_all([user1, user2, user3, user4])
    db_session.flush()

    # === GROUP ===
    group1 = Group(name="Pizza Party", owner_id=2)
    group1.users.extend([user1, user2, user3, user4])
    db_session.add(group1)
    db_session.flush()

    # === CATEGORY ===
    category1 = ExpenseCategory(
        name="yabloki",
        owner_id=user2.id,
    )
    db_session.add(category1)
    db_session.flush()

    # === EXPENSE (Pizza 1000 EUR) ===
    expense1 = Expense(
        group_id=group1.id,
        category_id=category1.id,
        title="Pizza",
        amount=1000,
        currency="EUR",
        expense_type="one-time",
        split_type="percent",
        payment_method="prepaid",
        periodicity=None,
        next_payment_date=datetime.now(timezone.utc) + timedelta(days=30),
        is_paid=False,
    )
    db_session.add(expense1)
    db_session.flush()

    # === PARTICIPANTS ===
    # Seva платит 750, Лёша должен 250
    share1 = ExpenseParticipant(
        expense_id=expense1.id,
        user_id=user1.id,
        amount=750,
        percentage=75,
        is_paid=True,
    )
    share2 = ExpenseParticipant(
        expense_id=expense1.id,
        user_id=user2.id,
        amount=250,
        percentage=25,
        is_paid=False,
    )
    db_session.add_all([share1, share2])

    # === PAYMENT ===
    payment1 = Payment(expense_id=expense1.id, payer_id=user1.id, amount=1000)
    db_session.add(payment1)

    # === DEBT ===
    debt1 = Debt(
        expense_id=expense1.id,
        debtor_id=user2.id,
        creditor_id=user1.id,
        amount=250,
        is_paid=False,
    )
    debt2 = Debt(
        expense_id=expense1.id,
        debtor_id=user1.id,
        creditor_id=user2.id,
        amount=500,
        is_paid=False,
    )
    debt3 = Debt(
        expense_id=expense1.id,
        debtor_id=user3.id,
        creditor_id=user2.id,
        amount=730,
        is_paid=True,
    )
    db_session.add_all([debt1, debt2, debt3])

    # Сохраняем изменения
    db_session.commit()

    return jsonify(
        {
            "status": "ok",
            "message": "Test data seeded!!!11!!!!!!!!!1!1!!!!!!!!!!11!!!!!!!!!!!!!!!!!1!!!1!!!!!!!!!!!!!!!!",
        }
    ), 201
