from flask import Blueprint, request
from flask_restful import Api, Resource

from server.db.models.__all_models import User, ExpenseCategory
from server.db.db_session import create_session
from server.app.utils import jwt_tokens

expense_categories_bp = Blueprint(
    "expense_categories_api",
    __name__,
    url_prefix="/expense_categories",
)

api = Api(expense_categories_bp)


class ExpenseCategoriesResource(Resource):
    @jwt_tokens.token_required
    def post(self, user_id):
        db_sess = create_session()
        try:
            data = request.get_json()
            name: str = data.get("name")

            if not name:
                return {"message": "expense category name is required"}, 400

            existing = db_sess.query(ExpenseCategory).filter_by(name=name).first()
            if existing:
                return {"message": "expense category already exists"}, 403

            user = db_sess.get(User, user_id)
            if not user:
                return {"message": "user not found"}, 404

            expense_category = ExpenseCategory(
                name=name,
                owner_id=user_id,
            )

            db_sess.add(expense_category)
            db_sess.commit()

            return {
                "message": "expense category created",
                "expense_category": expense_category.to_dict(),
            }

        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

        finally:
            db_sess.close()

    @jwt_tokens.token_required
    def delete(self, user_id, expense_category_id):
        db_sess = create_session()
        try:
            expense_category = db_sess.get(ExpenseCategory, expense_category_id)
            if not expense_category:
                return {"message": "expense category not found"}, 404

            if expense_category.owner_id != user_id:
                return {"message": "permission denied"}, 403

            db_sess.delete(expense_category)
            db_sess.commit()

            return {"message": "expense category deleted"}, 200

        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

        finally:
            db_sess.close()


api.add_resource(ExpenseCategoriesResource, "/<int:expense_category_id>", "/")
