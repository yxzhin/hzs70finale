from flask import Blueprint
from server.app.api.user import user_bp
from server.app.api.group import groups_bp
from server.app.api.user_group import user_groups_bp
from server.app.api.test import test_bp
from server.app.api.expense_category import expense_categories_bp

api_bp = Blueprint("api", __name__)

api_bp.register_blueprint(user_bp)
api_bp.register_blueprint(groups_bp)
api_bp.register_blueprint(user_groups_bp)
api_bp.register_blueprint(test_bp)
api_bp.register_blueprint(expense_categories_bp)
