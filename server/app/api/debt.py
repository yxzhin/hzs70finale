from flask import Blueprint
from flask_restful import Api, Resource

from server.db.models.__all_models import Debt
from server.db.db_session import create_session
from server.app.utils import jwt_tokens

debts_bp = Blueprint(
    "debts_api",
    __name__,
)

api = Api(debts_bp)


class DebtsResource(Resource):
    @jwt_tokens.token_required
    def get(self, user_id):
        db_sess = create_session()
        try:
            debts = db_sess.query(Debt).filter(Debt.creditor_id == user_id).all()
            debts_by_debtor = {}
            for debt in debts:
                debtor = debt.debtor
                if debtor.id not in debts_by_debtor:
                    debts_by_debtor[debtor.id] = {
                        "debtor": {
                            "id": debtor.id,
                            "username": debtor.username,
                        },
                        "total_amount": 0,
                        "debts": [],
                    }

                debts_by_debtor[debtor.id]["debts"].append(
                    {
                        "id": debt.id,
                        "amount": debt.amount,
                        "expense_id": debt.expense_id,
                        "is_paid": debt.is_paid,
                    }
                )
                debts_by_debtor[debtor.id]["total_amount"] += debt.amount

            response = {
                "creditor_id": user_id,
                "debts_by_debtor": list(debts_by_debtor.values()),
            }

            return response, 200

        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

        finally:
            db_sess.close()


api.add_resource(DebtsResource, "/debts")
