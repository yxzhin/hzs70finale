import json
from datetime import datetime
from flask import Blueprint, request
from flask_restful import Api, Resource

from server.db.models.__all_models import (
    User,
    Group,
    UserGroup,
    Expense,
    ExpenseParticipant,
    Payment,
    Debt,
)
from server.db.db_session import create_session
from server.app.utils import jwt_tokens

expense_bp = Blueprint(
    "expense_api",
    __name__,
    url_prefix="/expense",
)

api = Api(expense_bp)


class ExpenseResource(Resource):
    def get(self, expense_id):
        db_sess = create_session()
        try:
            expense = db_sess.get(Expense, expense_id)
            if not expense:
                return {"message": "Expense not found"}, 404
            return expense.to_dict(), 200
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500
        finally:
            db_sess.close()

    @jwt_tokens.token_required
    def post(self, user_id):
        db_sess = create_session()
        try:
            data = request.get_json()

            # 1. Validation of required fields
            required_fields = [
                "group_id", "title", "amount", "currency",
                "expense_type", "split_type", "payment_method",
                "next_payment_date", "is_paid", "participants"
            ]
            for field in required_fields:
                if field not in data:
                    return {"message": f"{field} is required"}, 400

            group_id = data["group_id"]

            # ✅ Проверка, состоит ли пользователь в группе
            user_in_group = db_sess.query(UserGroup).filter_by(user_id=user_id, group_id=group_id).first()
            if not user_in_group:
                return {"message": "User is not a member of this group"}, 403

            # if Expense is paid, sum of Payments must be the same as the amount
            is_paid = data["is_paid"]
            payments = data.get("payments", [])

            total_payment_amount = sum(p["amount"] for p in payments) if payments else 0

            if is_paid:
                if not payments:
                    return {"message": "Expense is marked as paid, but no payments were provided"}, 400
                if total_payment_amount != data["amount"]:
                    return {
                        "message": f"Total payments ({total_payment_amount}) do not match the expense amount ({data['amount']})"
                    }, 400

            # 2. Creating a Expence
            expense = Expense(
                group_id=data["group_id"],
                title=data["title"],
                amount=data["amount"],
                currency=data["currency"],
                expense_type=data["expense_type"],
                split_type=data["split_type"],
                payment_method=data["payment_method"],
                periodicity=data.get("periodicity"),
                next_payment_date=datetime.fromisoformat(data["next_payment_date"]), # 🔥 Исправлено здесь
                is_paid=data["is_paid"],
            )

            db_sess.add(expense)
            db_sess.flush()

            # 3. Adding expense participants
            for p in data["participants"]:
                participant = ExpenseParticipant(
                    expense_id=expense.id,
                    user_id=p["user_id"],
                    amount=p["amount"],
                    percentage=p.get("percentage"),
                    is_paid=False
                )
                db_sess.add(participant)

            # 4. Adding payments (if any)
            total_paid_by = {}
            for pay in payments:
                payer_id = pay["payer_id"]
                amount = pay["amount"]
                payment = Payment(
                    expense_id=expense.id,
                    payer_id=payer_id,
                    amount=amount
                )
                db_sess.add(payment)
                total_paid_by[payer_id] = total_paid_by.get(payer_id, 0) + amount

            # 5. Generating debts (only if there were any payments)
            if total_paid_by:
                total_owed_by = {}
                for part in data["participants"]:
                    user_id = part["user_id"]
                    amount = part["amount"]
                    total_owed_by[user_id] = total_owed_by.get(user_id, 0) + amount

                for debtor_id, owed in total_owed_by.items():
                    paid = total_paid_by.get(debtor_id, 0)
                    net = owed - paid

                    if net <= 0:
                        continue  # already settled

                    creditors = [
                        (cid, amt) for cid, amt in total_paid_by.items()
                        if cid != debtor_id and amt > 0
                    ]
                    for creditor_id, available in creditors:
                        if net == 0:
                            break

                        debt_amount = min(available, net)
                        db_sess.add(Debt(
                            debtor_id=debtor_id,
                            creditor_id=creditor_id,
                            amount=debt_amount,
                            expense_id=expense.id,
                            is_paid=False
                        ))

                        total_paid_by[creditor_id] -= debt_amount
                        net -= debt_amount

            db_sess.commit()
            return {"message": "Expense added successfully", "expense_id": expense.id}, 201

        except Exception as e:
            db_sess.rollback()
            return {"message": f"An error occurred: {str(e)}"}, 500
        finally:
            db_sess.close()


class AllExpensesOfGroupResource(Resource):
    def get(self, group_id):
        db_sess = create_session()
        try:
            all_expenses = (
                db_sess.query(Expense).filter(Expense.group_id == group_id).all()
            )
            if not all_expenses:
                return {"message": "No expenses found"}, 404
            return [expense.to_dict() for expense in all_expenses], 200
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500
        finally:
            db_sess.close()


class ExpenseHistoryResource(Resource):
    @jwt_tokens.token_required
    def post(self, user_id):
        db_sess = create_session()
        try:
            data = request.get_json()
            group_id: int = data.get("group_id")
            items_per_page: int = data.get("items_per_page")
            page: int = data.get("page")
            filter_is_paid = data.get("filter_is_paid")

            if not items_per_page:
                items_per_page = 10

            if not group_id:
                return {"message": "group id is required"}, 400

            user = db_sess.get(User, user_id)
            if not user:
                return {"message": "user not found"}, 404

            group = db_sess.get(Group, group_id)
            if not group:
                return {"message": "group not found"}, 404

            if group.owner_id != user_id:
                return {"message": "permission denied"}

            query = db_sess.query(Expense).filter(Expense.group_id == group_id)

            if filter_is_paid is not None:
                query = query.filter(Expense.is_paid == bool(filter_is_paid))

            total = query.count()
            total_pages = (total + items_per_page - 1) // items_per_page
            expenses = (
                query.offset((page - 1) * items_per_page).limit(items_per_page).all()
            )
            items = [item.to_dict() for item in expenses]

            return {
                "page": page,
                "items_per_page": items_per_page,
                "total_items": len(items),
                "total_pages": total_pages,
                "expenses": items,
            }, 200

        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500
        finally:
            db_sess.close()


api.add_resource(ExpenseResource, "/<int:expense_id>", "/")
api.add_resource(AllExpensesOfGroupResource, "/group/<int:group_id>")
api.add_resource(ExpenseHistoryResource, "/history")
