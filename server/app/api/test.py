from flask import Blueprint, jsonify
from datetime import datetime, timedelta, timezone
from random import randint, choice, uniform
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

    # --- USERS ---
    usernames = [
        "seva", "lesha", "filip", "grisha",
        "anna", "olga", "max", "daria",
        "ivan", "natalia"
    ]
    users = []
    for uname in usernames:
        user = User(username=uname, hashed_password="")
        user.set_password("password")
        db_session.add(user)
        users.append(user)
    db_session.flush()

    # --- GROUPS ---
    groups = [
        Group(name="Pizza Party", owner_id=users[1].id),   # Lesha
        Group(name="Weekend Trip", owner_id=users[4].id),  # Anna
        Group(name="Office Lunch", owner_id=users[0].id),  # Seva
    ]

    for group in groups:
        # Add random users to group
        group_users = set()
        while len(group_users) < randint(3, 6):
            group_users.add(choice(users))
        group.users.extend(list(group_users))
        db_session.add(group)
    db_session.flush()

    # --- EXPENSE CATEGORIES ---
    category_names = ["Food", "Travel", "Entertainment", "Groceries", "Utilities", "Health", "Books"]
    categories = []
    for name in category_names:
        owner = choice(users)
        category = ExpenseCategory(name=name, owner_id=owner.id)
        db_session.add(category)
        categories.append(category)
    db_session.flush()

    # --- EXPENSES ---
    expenses = []
    currencies = ["EUR", "USD", "RUB", "GBP"]
    expense_types = ["one-time", "recurring"]
    split_types = ["equal", "percent", "amount"]
    payment_methods = ["prepaid", "cash", "card"]

    for group in groups:
        num_expenses = randint(3, 6)
        for _ in range(num_expenses):
            category = choice(categories)
            title = f"{choice(['Dinner', 'Taxi', 'Concert', 'Groceries', 'Hotel'])} Expense"
            amount = round(uniform(50, 2000), 2)
            currency = choice(currencies)
            expense_type = choice(expense_types)
            split_type = choice(split_types)
            payment_method = choice(payment_methods)
            periodicity = None
            next_payment_date = None
            if expense_type == "recurring":
                periodicity = choice(["monthly", "weekly"])
                next_payment_date = datetime.now(timezone.utc) + timedelta(days=randint(5, 40))
            expense = Expense(
                group_id=group.id,
                category_id=category.id,
                title=title,
                amount=amount,
                currency=currency,
                expense_type=expense_type,
                split_type=split_type,
                payment_method=payment_method,
                periodicity=periodicity,
                next_payment_date=next_payment_date,
                is_paid=False,
            )
            db_session.add(expense)
            db_session.flush()

            # --- PARTICIPANTS ---
            participants = list(group.users)
            total_percentage = 100
            shares = []
            if split_type == "equal":
                share_amount = round(amount / len(participants), 2)
                for user in participants:
                    shares.append({
                        "user_id": user.id,
                        "amount": share_amount,
                        "percentage": round(100 / len(participants), 2),
                        "is_paid": choice([True, False]),
                    })
            elif split_type == "percent":
                remaining_percentage = 100
                for i, user in enumerate(participants):
                    if i == len(participants) - 1:
                        perc = remaining_percentage
                    else:
                        perc = randint(5, remaining_percentage - 5*(len(participants)-i-1))
                    remaining_percentage -= perc
                    amount_user = round(amount * perc / 100, 2)
                    shares.append({
                        "user_id": user.id,
                        "amount": amount_user,
                        "percentage": perc,
                        "is_paid": choice([True, False]),
                    })
            else:  # split_type == "amount"
                remaining_amount = amount
                for i, user in enumerate(participants):
                    if i == len(participants) - 1:
                        share_amount = remaining_amount
                    else:
                        share_amount = round(uniform(5, remaining_amount - 5*(len(participants)-i-1)), 2)
                    remaining_amount -= share_amount
                    shares.append({
                        "user_id": user.id,
                        "amount": share_amount,
                        "percentage": round(share_amount / amount * 100, 2),
                        "is_paid": choice([True, False]),
                    })

            # Add ExpenseParticipant entries
            for share in shares:
                ep = ExpenseParticipant(
                    expense_id=expense.id,
                    user_id=share["user_id"],
                    amount=share["amount"],
                    percentage=share["percentage"],
                    is_paid=share["is_paid"],
                )
                db_session.add(ep)

            # --- PAYMENTS ---
            payer = choice(participants)
            payment_amount = round(uniform(amount * 0.5, amount), 2)
            payment = Payment(
                expense_id=expense.id,
                payer_id=payer.id,
                amount=payment_amount
            )
            db_session.add(payment)

            # --- DEBTS ---
            # For simplicity, assume debts exist between participants who didn't pay fully
            for share in shares:
                if share["user_id"] != payer.id and not share["is_paid"]:
                    debt_amount = share["amount"]
                    debt = Debt(
                        expense_id=expense.id,
                        debtor_id=share["user_id"],
                        creditor_id=payer.id,
                        amount=debt_amount,
                        is_paid=False,
                    )
                    db_session.add(debt)

            expenses.append(expense)

    db_session.commit()

    return jsonify(
        {
            "status": "ok",
            "message": "Realistic test data seeded successfully!",
            "users_count": len(users),
            "groups_count": len(groups),
            "categories_count": len(categories),
            "expenses_count": len(expenses),
        }
    ), 201
