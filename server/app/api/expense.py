from flask import Blueprint, request
from flask_restful import Api, Resource

from server.db.models.__all_models import (
    User,
    Group,
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


api.add_resource(ExpenseResource, "/<int:expense_id>")
api.add_resource(AllExpensesOfGroupResource, "/group/<int:group_id>")
api.add_resource(ExpenseHistoryResource, "/history")
